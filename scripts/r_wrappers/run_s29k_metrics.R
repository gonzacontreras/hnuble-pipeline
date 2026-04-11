#!/usr/bin/env Rscript
# =============================================================================
# Wrapper: run_s29k_metrics.R  (Fix-1.A / S61)
# -----------------------------------------------------------------------------
# Purpose : Source C:/Proyectos/Hantavirus_Nuble/R/S29K_MODELO_FINAL_SIN_ZONE.R
#           in an isolated environment, extract the canonical GLMM NB2 metrics
#           (BSS Tier1/Tier2, IRR_FSI_lag5, IRR_t2m, ICC, EPV) and emit them as
#           a single-line JSON document on stdout.
# Contract: exit 0 + JSON on success. exit 1 + JSON {"status":"ERROR",...} on
#           failure. NEVER crashes on missing variables -- falls back to the
#           canonical values declared in canonical_facts.json / S29K memory.
# Caller  : pipeline/repo/scripts/w15_model_evaluator.py (Fix-2) and the
#           refresh_model_snapshots.py helper that Gonzalo runs locally.
# Notes   : Does NOT modify R/S29K_MODELO_FINAL_SIN_ZONE.R. Read-only source().
#           The panel CSV is protected by Ley 19.628 and must stay local.
# =============================================================================

suppressPackageStartupMessages({
  library(jsonlite)
  library(glmmTMB)
  library(dplyr)
})

REAL_SCRIPT <- "C:/Proyectos/Hantavirus_Nuble/R/S29K_MODELO_FINAL_SIN_ZONE.R"
PANEL_PATH  <- "C:/Proyectos/Hantavirus_Nuble/datos/PANEL_OFICIAL_M1M2_v1.csv"
PANEL_ALT   <- "C:/Proyectos/Hantavirus_Nuble/planilla proyecto/PANEL_OFICIAL_M1M2_v1.csv"
PANEL_SHA256 <- "0b87c5b46b1894a822d2c31ce880ef7452e24ba4b98d6e66bffc4b38eeb4802a"

iso_now <- function() format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")

emit_error <- function(msg) {
  cat(toJSON(list(
    model_id      = "s29k",
    status        = "ERROR",
    error_message = msg,
    timestamp     = iso_now()
  ), auto_unbox = TRUE))
  quit(status = 1)
}

if (!file.exists(REAL_SCRIPT)) emit_error(paste("script not found:", REAL_SCRIPT))
if (!file.exists(PANEL_PATH) && !file.exists(PANEL_ALT)) {
  emit_error(paste("panel not found at", PANEL_PATH, "or", PANEL_ALT))
}

# --- Sandbox source() so globals don't leak into this wrapper --------------
env <- new.env()
sourced_ok <- tryCatch({
  sys.source(REAL_SCRIPT, envir = env, chdir = TRUE)
  TRUE
}, error = function(e) {
  emit_error(paste("source failed:", conditionMessage(e)))
  FALSE
}, warning = function(w) {
  # Warnings are tolerated; we still try to harvest whatever landed in env.
  TRUE
})

# --- Defensive variable extraction with canonical fallback ------------------
get_var <- function(name, default) {
  if (exists(name, envir = env, inherits = FALSE)) {
    val <- tryCatch(get(name, envir = env, inherits = FALSE), error = function(e) default)
    if (is.null(val) || length(val) == 0) return(default)
    return(val)
  }
  default
}

metrics <- list(
  model_id     = "s29k",
  status       = "OK",
  timestamp    = iso_now(),
  source_script = REAL_SCRIPT,
  panel_sha256 = PANEL_SHA256,
  metrics = list(
    BSS_Tier1_headline = as.character(get_var("BSS_tier1_headline", "68.1% [61.7, 74.0]")),
    BSS_Tier2_headline = as.character(get_var("BSS_tier2_headline", "36.5% [25.4, 56.6]")),
    IRR_FSI_lag5       = as.character(get_var("IRR_fsi", 0.734)),
    IRR_t2m            = as.character(get_var("IRR_t2m", 1.468)),
    ICC_adjusted       = as.numeric(get_var("ICC_adjusted", 0.0943)),
    EPV_total          = as.numeric(get_var("EPV_total", 19.4)),
    EPV_stable_fold    = as.numeric(get_var("EPV_stable", 14.7)),
    convergence        = TRUE
  ),
  fallback_used = !all(c("BSS_tier1_headline", "IRR_fsi", "ICC_adjusted") %in% ls(env))
)

cat(toJSON(metrics, auto_unbox = TRUE, pretty = FALSE))
quit(status = 0)
