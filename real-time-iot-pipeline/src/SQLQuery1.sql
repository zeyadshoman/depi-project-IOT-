CREATE TABLE WeatherStation_Pro (
    Timestamp datetime,
    DeviceID nvarchar(100),
    DeviceType nvarchar(100),
    Location nvarchar(100),
    Zone nvarchar(100),
    Temperature_C float,
    Humidity_pct float,
    WindSpeed_kmh float,
    WindDirection nvarchar(10),
    Rainfall_mm float,
    CloudCoverage_pct float,
    UV_Index float,
    Pressure_hPa float,
    Battery_pct float,
    AlertLevel int,
    AlertType nvarchar(100),
    Advisory nvarchar(300)
);
Select * From WeatherStation_Pro

