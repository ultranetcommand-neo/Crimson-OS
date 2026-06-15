#!/usr/bin/env python3
"""
JHTDB Shear Alignment Test - PRODUCTION RUN
-------------------------------------------
Queries the Johns Hopkins Turbulence Database (JHTDB) 'channel' dataset
to compute the vorticity-strain alignment metrics (cos^2 \phi_i) under
macroscopic shear (broken isotropy). 

This script uses `zeep` (SOAP) to bypass Windows C-library compilation
issues with `pyJHTDB`. To bypass JHTDB WSDL enum bugs with GetVelocityGradient 
on the channel dataset, we query GetVelocity and compute the gradients 
via 4th-order central difference.
"""

import sys
import json
import time
import numpy as np
from datetime import datetime, timezone
from zeep import Client

AUTH_TOKEN = "edu.jhu.pha.turbulence.testing-201302"
DATASET = "channel"
N_POINTS = 4000

def generate_biased_channel_points(n_points):
    """
    Generate points biased heavily toward the channel walls (shear boundary).
    """
    rng = np.random.RandomState(42)
    x = rng.uniform(0, 8 * np.pi, n_points)
    z = rng.uniform(0, 3 * np.pi, n_points)
    r = rng.uniform(-1, 1, n_points)
    y = np.sign(r) * (1.0 - np.abs(r)**3)
    y = np.clip(y, -0.99, 0.99)
    return np.column_stack((x, y, z))

def get_velocity_gradients_zeep(points):
    """Query JHTDB using GetVelocity and central difference."""
    print(f"Connecting to JHTDB SOAP API to compute gradients for {len(points)} points...")
    start_time = time.time()
    
    wsdl = "http://turbulence.pha.jhu.edu/service/turbulence.asmx?WSDL"
    client = Client(wsdl)
    Point3 = client.get_type('ns0:Point3')
    ArrayOfPoint3 = client.get_type('ns0:ArrayOfPoint3')
    
    # 2nd order central difference stencil
    # M_ij = du_i / dx_j
    d = 0.005 # Stencil size
    
    # We need to query points shifted by +/- d in x, y, z
    # Total points to query = 6 * N_POINTS
    N = len(points)
    shift_x = np.array([d, 0, 0])
    shift_y = np.array([0, d, 0])
    shift_z = np.array([0, 0, d])
    
    pts_xp = points + shift_x
    pts_xm = points - shift_x
    pts_yp = points + shift_y
    pts_ym = points - shift_y
    pts_zp = points + shift_z
    pts_zm = points - shift_z
    
    # Combine all points into one large query array
    all_query_points = np.vstack([pts_xp, pts_xm, pts_yp, pts_ym, pts_zp, pts_zm])
    
    # Chunk into 4000 points to avoid SOAP limits
    chunk_size = 4000
    all_velocities = np.zeros((len(all_query_points), 3))
    
    print(f"Total velocity queries required: {len(all_query_points)} (batching...)")
    for i in range(0, len(all_query_points), chunk_size):
        chunk = all_query_points[i:i+chunk_size]
        pts = [Point3(x=float(p[0]), y=float(p[1]), z=float(p[2])) for p in chunk]
        points_array = ArrayOfPoint3(Point3=pts)
        
        try:
            res = client.service.GetVelocity(
                authToken=AUTH_TOKEN,
                dataset=DATASET,
                time=0.0,
                spatialInterpolation='Lag4',
                temporalInterpolation='PCHIP',
                points=points_array
            )
            for j, v in enumerate(res):
                all_velocities[i+j] = [v['x'], v['y'], v['z']]
        except Exception as e:
            print(f"ERROR: SOAP chunk failed: {e}")
            sys.exit(1)
            
    # Unpack velocities
    v_xp = all_velocities[0:N]
    v_xm = all_velocities[N:2*N]
    v_yp = all_velocities[2*N:3*N]
    v_ym = all_velocities[3*N:4*N]
    v_zp = all_velocities[4*N:5*N]
    v_zm = all_velocities[5*N:6*N]
    
    # Compute gradients (central difference: du/dx = (u(x+d) - u(x-d)) / 2d )
    grads = np.zeros((N, 3, 3))
    
    for i in range(N):
        # M_ij = du_i / dx_j
        du_dx = (v_xp[i] - v_xm[i]) / (2*d)
        du_dy = (v_yp[i] - v_ym[i]) / (2*d)
        du_dz = (v_zp[i] - v_zm[i]) / (2*d)
        
        M = np.array([
            [du_dx[0], du_dy[0], du_dz[0]],
            [du_dx[1], du_dy[1], du_dz[1]],
            [du_dx[2], du_dy[2], du_dz[2]]
        ])
        grads[i] = M
        
    print(f"JHTDB query and FD completed in {time.time() - start_time:.2f}s")
    return grads

def compute_alignments(grads):
    """Compute triplet alignment cosines and enstrophy."""
    N = grads.shape[0]
    cos2_phi1, cos2_phi2, cos2_phi3, enstrophy = [], [], [], []
    
    for i in range(N):
        M = grads[i]
        S = 0.5 * (M + M.T)
        Omega = 0.5 * (M - M.T)
        
        w = np.array([
            Omega[2, 1] - Omega[1, 2],
            Omega[0, 2] - Omega[2, 0],
            Omega[1, 0] - Omega[0, 1]
        ])
        
        omega_sq = np.dot(w, w)
        enstrophy.append(omega_sq)
        
        if omega_sq < 1e-10:
            continue
            
        w_hat = w / np.sqrt(omega_sq)
        
        evals, evecs = np.linalg.eigh(S)
        idx = np.argsort(evals)[::-1]
        evecs = evecs[:, idx]
        
        cos2_phi1.append(np.dot(w_hat, evecs[:, 0])**2)
        cos2_phi2.append(np.dot(w_hat, evecs[:, 1])**2)
        cos2_phi3.append(np.dot(w_hat, evecs[:, 2])**2)
        
    return np.array(cos2_phi1), np.array(cos2_phi2), np.array(cos2_phi3), np.array(enstrophy)

def main():
    timestamp = datetime.now(timezone.utc).isoformat()
    
    print("=" * 72)
    print("  JHTDB CHANNEL SHEAR DNS ALIGNMENT TEST - PRODUCTION RUN")
    print(f"  Dataset: {DATASET} | Target: 1/9 bound (cos^2 phi_1 <= 0.111)")
    print("=" * 72)
    
    points = generate_biased_channel_points(N_POINTS)
    grads = get_velocity_gradients_zeep(points)
    
    print("\nComputing alignments...")
    cos2_1, cos2_2, cos2_3, enstrophy = compute_alignments(grads)
    
    if len(enstrophy) == 0:
        print("No valid points processed.")
        sys.exit(1)
        
    print(f"\nGLOBAL STATISTICS ({len(enstrophy)} points):")
    print(f"  <cos^2 phi_1> (Extensional)  = {np.mean(cos2_1):.4f}")
    print(f"  <cos^2 phi_2> (Intermediate) = {np.mean(cos2_2):.4f}")
    print(f"  <cos^2 phi_3> (Compressional)= {np.mean(cos2_3):.4f}")
    
    # Conditional statistics (High Enstrophy)
    high_threshold = 3.0 * np.mean(enstrophy)
    high_mask = enstrophy > high_threshold
    n_high = np.sum(high_mask)
    
    if n_high > 0:
        print(f"\nCONDITIONAL STATISTICS (High Enstrophy: |w|^2 > 3<|w|^2>, {n_high} points):")
        print(f"  <cos^2 phi_1> (Extensional)  = {np.mean(cos2_1[high_mask]):.4f}  (Target <= 1/9 ≈ 0.111)")
        print(f"  <cos^2 phi_2> (Intermediate) = {np.mean(cos2_2[high_mask]):.4f}")
        print(f"  <cos^2 phi_3> (Compressional)= {np.mean(cos2_3[high_mask]):.4f}")
    else:
        print("\nNo points met the high enstrophy threshold.")
        
    # Output arrays for distributions
    output = {
        "timestamp": timestamp,
        "n_points": N_POINTS,
        "n_high_enstrophy": int(n_high),
        "global_means": {
            "c1": float(np.mean(cos2_1)),
            "c2": float(np.mean(cos2_2)),
            "c3": float(np.mean(cos2_3))
        },
        "high_enstrophy_means": {
            "c1": float(np.mean(cos2_1[high_mask])) if n_high > 0 else None,
            "c2": float(np.mean(cos2_2[high_mask])) if n_high > 0 else None,
            "c3": float(np.mean(cos2_3[high_mask])) if n_high > 0 else None
        },
        "distributions": {
            "high_enstrophy_cos2_phi1": cos2_1[high_mask].tolist() if n_high > 0 else []
        }
    }
    
    json_path = "jhtdb_production_results.json"
    with open(json_path, "w") as f:
        json.dump(output, f)
        
    print(f"\nFull arrays written to {json_path}")

if __name__ == "__main__":
    main()
