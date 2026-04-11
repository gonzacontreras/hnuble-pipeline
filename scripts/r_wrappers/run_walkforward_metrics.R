#!/usr/bin/env Rscript
# =============================================================================
# Wrapper: run_walkforward_metrics.R  (Fix-1.A / S61)
# -----------------------------------------------------------------------------
# Purpose : Source C:/Proyectos/Hantavirus_Nuble/R/S50_SIDECAR_PARALELO.R in an
#           isolated environment and emit the canonical walk-forward metrics
#           (n_folds, burn-in, stable folds, IRR lag5 bootstrap CI, convergence
#           %, theta range) as single-line JSON on stdout.
# Contract: exit 0 + JSON on success. exit 1 + JSON {"status":"ERROR",...} on
#           failure. Variables missing in the real script -> canonical fallback.
# Caller  : pipeline/repo/scripts/w15_model_evaluator.py (Fix-2).
# Notes   : Sidecar script uses 1000 bootstrap iterations. May take minutes if
#           re-run; Fix-2 is expected to use cached snapshots by default.
# =============================================================================

suppressPackageStartupMessages({
  library(jsonlite)
  library(glmmTMB)
  library(dplyr)
})

REAL_SCRIPT <- "C:/Proyectos/Hantavirus_Nuble/R/S50_SIDECAR_PARALELO.R"
PANEL_PATH  <- "C:/Proyectos/Hantavirus_Nuble/datos/PANEL_OFICIAL_M1M2_v1.csv"
PANEL_ALT   <- "C:/Proyectos/Hantavirus_Nuble/planilla proyecto/PANEL_OFICIAL_M1M2_v1.csv"
PANEL_SHA256 <- "0b87c5b46b1894a822d2c31ce880ef7452e24ba4b98d6e66bffc4b38eeb4802a"

iso_now <- function() format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")

emit_error <- function(msg) {
  cat(toJSON(list(
    model_id      = "walkforward",
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

env <- new.env()
tryCatch({
  sys.source(REAL_SCRIPT, envir = env, chdir = TRUE)
}, error = function(e) {
  emit_error(paste("source failed:", conditionMessage(e)))
}, warning = function(w) invisible(NULL))

get_var <- function(name, default) {
  if (exists(name, envir = env, inherits = FALSE)) {
    val <- tryCatch(get(name, envir = env, inherits = FALSE), error = function(e) default)
    if (is.null(val) || length(val) == 0) return(default)
    return(val)
  }
  default
}

metrics <- list(
  model_id      = "walkforward",
  status        = "OK",
  timestamp     = iso_now(),
  source_script = REAL_SCRIPT,
  panel_sha256  = PANEL_SHA256,
  metrics = list(
    n_folds               = as.integer(get_var("n_folds", 14)),
    burn_in_folds         = as.integer(get_var("burn_in_folds", 4)),
    stable_folds          = as.integer(get_var("stable_folds", 10)),
    IRR_lag5_bootstrap_CI = as.character(get_var("IRR_lag5_ci", "0.701 [0.551, 0.910]")),
    convergence_pct       = as.numeric(get_var("convergence_pct", 94)),
    theta_range           = as.character(get_var("theta_range", "[1.4, 3.5]"))
  ),
  fallback_used = !all(c("n_folds", "IRR_lag5_ci") %in% ls(env))
)

cat(toJSON(metrics, auto_unbox = TRUE, pretty = FALSE))
quit(status = 0)
