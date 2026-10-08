import Mathlib.Analysis.InnerProductSpace.Spectrum
import Mathlib.LinearAlgebra.Matrix.Spectrum

open Matrix LinearMap

theorem canonical_pullback_bounded 
    {n_global n_local : ℕ}
    (L_NS : Matrix (Fin n_global) (Fin n_global) ℝ)
    (J : Matrix (Fin n_global) (Fin n_local) ℝ)
    (h_herm : L_NS.IsHermitian)
    (P_sat : ℝ)
    (h_bound : ∀ x : Fin n_global → ℝ, x ≠ 0 → (star x ⬝ᵥ (L_NS *ᵥ x)) / (star x ⬝ᵥ x) ≤ P_sat) :
    ∀ v : Fin n_local → ℝ, v ≠ 0 → 
    let L_local := Jᵀ * L_NS * J
    ((star v ⬝ᵥ (L_local *ᵥ v)) / (star v ⬝ᵥ v)) ≤ P_sat * (LinearMap.toContinuousLinearMap (Matrix.toLin' J)).opNorm ^ 2 := by
  intro v hv
  dsimp
  sorry
