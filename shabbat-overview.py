SHABBAT_START = "16:29"  # Example start time (candle lighting)
SHABBAT_END = "17:13"    # Example end time (Havdalah)
UNIT_SYSTEM = "imperial"  # or "metric"

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

def convert_to_12hr_format(time_str):
    # Assuming the time_str is in 'HH:MM' format
    time_obj = datetime.strptime(time_str, '%H:%M')
    return time_obj.strftime('%I:%M %p')  # %I for 12-hour and %p for AM/PM

def celsius_to_fahrenheit(celsius_temp):
    return (celsius_temp * 9/5) + 32

def create_sun_path_image(zmanim, weather, filename):
    # Create the plot
    fig, ax = plt.subplots()
    for zman in zmanim:
        ax.plot(zmanim[zman], 0, 'ro')  # Plot zmanim times
        ax.text(zmanim[zman], 0.1, zman, rotation=45)

    # Add weather data (optional, based on your data)
    # for forecast in weather:
    #     ax.plot(forecast['time'], forecast['temperature'], 'bo')
    #     ax.text(forecast['time'], forecast['temperature'] + 0.1, forecast['forecast'], rotation=45)

    # Format the plot
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the plot as an image
    plt.savefig(filename)
    plt.close()

def create_pdf(sun_path_img, filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Convert Shabbat start and end times for imperial system
    shabbat_start = SHABBAT_START
    shabbat_end = SHABBAT_END
    if UNIT_SYSTEM == "imperial":
        shabbat_start = convert_to_12hr_format(SHABBAT_START)
        shabbat_end = convert_to_12hr_format(SHABBAT_END)

    # Shabbat Times
    c.drawString(100, height - 100, f"Shabbat Start: Friday {shabbat_start}")
    c.drawString(100, height - 120, f"Shabbat End: Saturday {shabbat_end}")

    # Weather Forecast
    c.drawString(100, height - 160, "Hourly Weather Forecast for Shabbat:")
    y = height - 180
    for forecast in weather:
        temp = forecast['temperature']
        time = forecast['time']
        if UNIT_SYSTEM == "imperial":
            temp = celsius_to_fahrenheit(temp)
            temp_unit = "°F"
            time = convert_to_12hr_format(time)
        else:
            temp_unit = "°C"

        c.drawString(100, y, f"{forecast['day']} {time} - {forecast['forecast']}, {temp}{temp_unit}")
        y -= 20
        if y < 50:  # Check to avoid writing off the page
            break

    # Add the sun path image at the bottom of the PDF
    c.drawImage(sun_path_img, 50, 50, width=500, height=100)  # Adjust size and position as needed

    c.save()

zmanim = {
    "Candle Lighting": datetime(2023, 4, 14, 18, 0),
    "Havdalah": datetime(2023, 4, 15, 19, 0)
}
# Weather Data spanning 25 hours of Shabbat
weather = [
    {"day": "Friday", "time": "18:00", "forecast": "Clear", "temperature": 15},
    {"day": "Friday", "time": "19:00", "forecast": "Partly Cloudy", "temperature": 14},
    # ... more data for Friday evening
    {"day": "Saturday", "time": "06:00", "forecast": "Sunny", "temperature": 12},
    # ... more data for Saturday
    {"day": "Saturday", "time": "19:00", "forecast": "Clear", "temperature": 15},
    # ... more data for Saturday evening
]


sun_path_filename = "sun_path.png"
create_sun_path_image(zmanim, weather, sun_path_filename)

pdf_filename = "Shabbat_Overview.pdf"
create_pdf(sun_path_filename, pdf_filename)
