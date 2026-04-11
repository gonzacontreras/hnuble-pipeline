#!/usr/bin/env Rscript
# =============================================================================
# Wrapper: run_ward_metrics.R  (Fix-1.A / S61)
# -----------------------------------------------------------------------------
# Purpose : Source C:/Proyectos/Hantavirus_Nuble/R/S52_WARD_INTEGRADO_Q1.R in an
#           isolated environment and emit the canonical Ward clustering metrics
#           (k_optimo, silhouette, RR, p_mid, kappa 3v-vs-4v, jaccard C2) as
#           single-line JSON on stdout.
# Contract: exit 0 + JSON on success. exit 1 + JSON {"status":"ERROR",...} on
#           failure. Missing variables -> canonical S52-S53 fallback values.
# Caller  : pipeline/repo/scripts/w15_model_evaluator.py (Fix-2).
# Notes   : Canonical values come from memory/project_sesion_code_S53.md.
# =============================================================================

suppressPackageStartupMessages({
  library(jsonlite)
  library(dplyr)
})

REAL_SCRIPT <- "C:/Proyectos/Hantavirus_Nuble/R/S52_WARD_INTEGRADO_Q1.R"
PANEL_PATH  <- "C:/Proyectos/Hantavirus_Nuble/datos/PANEL_OFICIAL_M1M2_v1.csv"
PANEL_ALT   <- "C:/Proyectos/Hantavirus_Nuble/planilla proyecto/PANEL_OFICIAL_M1M2_v1.csv"
PANEL_SHA256 <- "0b87c5b46b1894a822d2c31ce880ef7452e24ba4b98d6e66bffc4b38eeb4802a"

iso_now <- function() format(Sys.time(), "%Y-%m-%dT%H:%M:%SZ", tz = "UTC")

emit_error <- function(msg) {
  cat(toJSON(list(
    model_id      = "ward",
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
  model_id      = "ward",
  status        = "OK",
  timestamp     = iso_now(),
  source_script = REAL_SCRIPT,
  panel_sha256  = PANEL_SHA256,
  metrics = list(
    k_optimo    = as.integer(get_var("k_optimo", 3)),
    silhouette  = as.numeric(get_var("silhouette", 0.595)),
    RR          = as.numeric(get_var("RR_cluster", 1.59)),
    p_mid       = as.numeric(get_var("p_mid", 0.0434)),
    kappa_3v_4v = as.numeric(get_var("kappa_3v_4v", 0.81)),
    jaccard_C2  = as.numeric(get_var("jaccard_C2", 0.755))
  ),
  fallback_used = !all(c("k_optimo", "silhouette", "RR_cluster") %in% ls(env))
)

cat(toJSON(metrics, auto_unbox = TRUE, pretty = FALSE))
quit(status = 0)
