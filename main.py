# main.py
# Original code from section "Entry point" - moved as-is.
# WIRING layer: decides the ORDER of the steps, not how they work.
# This is the file you run:  python main.py

# ==========================================================
# >>> ADDED FOR DATA FLOW (START)
# ==========================================================
# main() calls five functions that now live in four different modules.
# These imports pull each function into this file so main() can call it.
#
# Think of main.py as a relay coach handing the baton between runners:
#   run_weather_fetch()   (fetch.py)    -> returns raw_weather   (a dict)
#   validate_weather()    (validate.py) -> takes raw_weather,
#                                          returns report        (a Weather)
#   save_weather_report() (storage.py)  -> takes report, saves a row
#
# The data itself moves through the RETURN VALUES and ARGUMENTS in main().
# These imports only make the functions reachable.
#
# NOTE: importing storage also imports models.py, which registers the
# WeatherRecord table. That has to happen BEFORE init_db() runs, or
# init_db() would create no table. The import below guarantees it.
from weather_pipeline.database import init_db
from weather_pipeline.fetch import run_weather_fetch
from weather_pipeline.validate import validate_weather
from weather_pipeline.storage import save_weather_report, print_db
# ==========================================================
# <<< ADDED FOR DATA FLOW (END)
# ==========================================================


# =================================================
# 5. Entry point
# =================================================

def main():
    print("MAIN")
    init_db()
    raw_weather = run_weather_fetch()
    report = validate_weather(raw_weather)
    if report is not None:
        save_weather_report(report)
        # print_db()



if __name__ == "__main__":
    main()
    print_db()