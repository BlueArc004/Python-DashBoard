from pathlib import Path
import sys
import serial
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import csv
from tkinter import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Projects\build\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


continue_animation = True
ser = None


def update_plot_gyro(frame):
    global ser
    try:
        value = ser.readline().decode().strip()
        data_list = value.split(',')

        gyro_x = float(data_list[3])
        gyro_y = float(data_list[4])
        gyro_z = float(data_list[5])

        
        gyro_x_data.append(gyro_x)
        gyro_y_data.append(gyro_y)
        gyro_z_data.append(gyro_z)

        gyro_x_line.set_data(range(len(gyro_x_data)), gyro_x_data)
        gyro_y_line.set_data(range(len(gyro_y_data)), gyro_y_data)
        gyro_z_line.set_data(range(len(gyro_z_data)), gyro_z_data)

        gx.relim()
        gx.autoscale_view()

    except ValueError:
        pass

def update_plot_accelerometer(frame):
    global ser
    try:
        value = ser.readline().decode().strip()
        data_list = value.split(',')

        accelerometer_x = float(data_list[6])
        accelerometer_y = float(data_list[7])
        accelerometer_z = float(data_list[8])

        
        accelerometer_x_data.append(accelerometer_x)
        accelerometer_y_data.append(accelerometer_y)
        accelerometer_z_data.append(accelerometer_z)

        accelerometer_x_line.set_data(range(len(accelerometer_x_data)), accelerometer_x_data)
        accelerometer_y_line.set_data(range(len(accelerometer_y_data)), accelerometer_y_data)
        accelerometer_z_line.set_data(range(len(accelerometer_z_data)), accelerometer_z_data)

        accx.relim()
        accx.autoscale_view()

    except ValueError:
        pass

def update_plot_pressure(frame):
    global ser
    try:
        value = ser.readline().decode().strip()
        data_list = value.split(',')
        pressure_value = float(data_list[1])

        pressure_data.append(pressure_value)
    
        pressure_label.config(text=f"Pressure: {pressure_value} Pa")
        line_pressure.set_data(range(len(pressure_data)), pressure_data)
        px.relim()
        px.autoscale_view()

    except ValueError:
        pass



def update_plot_temperature(frame):
    global ser
    try:
        value = ser.readline().decode().strip()
        data_list = value.split(',')
        temperature_value = float(data_list[0])
        #  altitude_value = float(data_list[2])
        # temperature_value = float(data_list[0])
        # temperature_data.append((altitude_value, temperature_value))
        # line_temperature.set_data(*zip(*temperature_data))
        temperature_data.append(temperature_value)
        temperature_label.config(text=f"Temperature: {temperature_value} °C")
        line_temperature.set_data(range(len(temperature_data)), temperature_data)
        tx.relim()
        tx.autoscale_view()
    except ValueError:
        pass

def update_plot_alt(frame):
    global ser
    try:
        value = ser.readline().decode().strip()
        data_list = value.split(',')
        alt_value = float(data_list[2])
        alt_data.append(alt_value)
        altitude_label.config(text=f"Altitude: {alt_value} m")
        line_alt.set_data(range(len(alt_data)), alt_data)
        ax.relim()
        ax.autoscale_view()
    except ValueError:
        pass
def update_serial_data():
    try:
        value = ser.readline().decode().strip()
        serial_data_var.set(f"Serial Data: {value}")
    except ValueError:
        pass


def start_animation():
    global ser
    # com_port = com_port_var.get()
    # baud_rate = baud_rate_var.get()
    # ser = serial.Serial(com_port,int(baud_rate))
    update_plot_alt(None)
    update_plot_gyro(None)
    update_plot_temperature(None)
    update_plot_pressure(None)
    update_plot_accelerometer(None)
    update_serial_data()
    fig.canvas.draw()
    fig_1.canvas.draw()
    fig_t.canvas.draw()
    fig_p.canvas.draw()
    fig_acc.canvas.draw()

    if continue_animation:
        window.after(10, start_animation)


def button():
    global continue_animation
    continue_animation = True
    start_animation()

def stop_animation():
    global continue_animation
    continue_animation = False

def export_to_csv():
    data = zip(alt_data, pressure_data, temperature_data,gyro_x_data,gyro_y_data,gyro_z_data)
    csv_file_path = "D:\csv\export.csv"

    with open(csv_file_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Altitude (m)", "Pressure (Pa)", "Temperature (°C)"])
        csv_writer.writerows(data)

#ser = serial.Serial("COM4",115200)

alt_data = []
pressure_data = []
temperature_data = []
gyro_x_data = []
gyro_y_data = []
gyro_z_data = []
accelerometer_x_data = []
accelerometer_y_data = []
accelerometer_z_data = []


fig, ax = plt.subplots(figsize=(4.5, 5), facecolor='#000000')
ax.set_title('Altitude', color='white')
ax.set_ylabel('Altitude (m)', color='white')
ax.set_xlabel('Time', color='white')
ax.tick_params(colors='white')
ax.set_facecolor("#000000")
ax.patch.set_alpha(0.5)
line_alt, = ax.plot([])

fig_p, px = plt.subplots(figsize=(4.5, 5), facecolor='#000000')
px.set_title('Pressure', color='white')
px.set_ylabel('Pressure (Pa)', color='white')
px.set_xlabel('Time', color='white')
px.tick_params(colors='white')
px.set_facecolor("#000000")
px.patch.set_alpha(0.5)
line_pressure, = px.plot([])

fig_1, gx = plt.subplots(figsize=(4.5, 5), facecolor='#000000')
gx.set_title('Gyro', color='white')
gx.set_ylabel('Value', color='white')
gx.set_xlabel('Time', color='white')
gx.tick_params(colors='white')
gx.set_facecolor("#000000")
gx.patch.set_alpha(0.5)
accelerometer_x_line, = gx.plot([])
accelerometer_y_line, = gx.plot([])
accelerometer_z_line, = gx.plot([])

fig_acc, accx = plt.subplots(figsize=(4.5, 5), facecolor='#000000')
accx.set_title('Accelerometer', color='white')
accx.set_ylabel('Value', color='white')
accx.set_xlabel('Time', color='white')
accx.tick_params(colors='white')
accx.set_facecolor("#000000")
accx.patch.set_alpha(0.5)
gyro_x_line, = accx.plot([])
gyro_y_line, = accx.plot([])
gyro_z_line, = accx.plot([])

fig_t, tx = plt.subplots(figsize=(4.5, 5), facecolor='#000000')
tx.set_title('Temperature', color='white')
tx.set_ylabel('Temperature (°C)', color='white')
tx.set_xlabel('Time', color='white')
tx.tick_params(colors='white')
tx.set_facecolor("#000000")
tx.patch.set_alpha(0.5)
line_temperature, = tx.plot([])

window = tk.Tk()
window.geometry("1920x1080")
window.configure(bg="#000000")


# image_path = "D:/Projects/build/build/assets/frame0/avinya-clean AF.png"
# img = PhotoImage(file=image_path)

canvas = tk.Canvas(
    window,
    bg="#000000",
    height=1080,
    width=1920,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

canvas.place(x=0, y=0, relwidth=1, relheight=1)
canvas.create_rectangle(
    2.0,
    660.0,
    1918.0,
    1100.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    573.0,
    31.0,
    862.0,
    218.0,
    fill="#FFF9F9",
    outline="")

canvas.create_rectangle(
    575.0,
    33.0,
    860.0,
    216.0,
    fill="#0A0A0A",
    outline="")

canvas.create_rectangle(
    696.0,
    89.0,
    823.0,
    120.0,
    fill="#555252",
    outline="")

canvas.create_rectangle(
    57.0,
    581.0,
    232.0,
    612.0,
    fill="#555252",
    outline="")

canvas.create_text(
    607.0,
    92.0,
    anchor="nw",
    text="NET_ID",
    fill="#FFFFFF",
    font=("Inter", 20 * -1)
)

canvas.create_rectangle(
    697.0,
    169.0,
    824.0,
    200.0,
    fill="#555252",
    outline="")

canvas.create_text(
    598.0,
    133.0,
    anchor="nw",
    text="COM Port",
    fill="#FFFFFF",
    font=("Inter", 20 * -1)
)

canvas.create_rectangle(
    697.0,
    130.0,
    824.0,
    161.0,
    fill="#555252",
    outline="")

canvas.create_text(
    602.0,
    172.0,
    anchor="nw",
    text="Baudrate",
    fill="#FFFFFF",
    font=("Inter", 20 * -1)
)


canvas.create_rectangle(
    3.0,
    31.0,
    342.0,
    510.0,
    fill="#FFFFFF",
    outline="")


canvas.create_rectangle(
    5.0,
    33.0,
    340.0,
    508.0,
    fill="#050505",
    outline="")


canvas.create_text(
    171.0,
    382.0,
    anchor="nw",
    text="40ms^-2",
    fill="#FFFFFF",
    font=("Inter", 20 * -1)
)


canvas.create_text(
    17.0,
    382.0,
    anchor="nw",
    text="Accelerometer:",
    fill="#FFFFFF",
    font=("Inter", 20 * -1)
)

# canvas.create_text(
#     172.0,
#     295.0,
#     anchor="nw",
#     text="ON",
#     fill="#12EF0D",
#     font=("Inter", 20 * -1)
# )

# canvas.create_text(
#     15.0,
#     295.0,
#     anchor="nw",
#     text="Camera Status :",
#     fill="#FFFFFF",
#     font=("Inter", 20 * -1)
# )

canvas.create_text(
    254.0,
    255.0,
    anchor="nw",
    text="3V",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

canvas.create_text(
    209.0,
    223.0,
    anchor="nw",
    text="Battery Voltage",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

canvas.create_text(
    253.0,
    196.0,
    anchor="nw",
    text="75%",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

canvas.create_text(
    172.0,
    264.0,
    anchor="nw",
    text="3",
    fill="#FFFFFF",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    133.0,
    225.0,
    anchor="nw",
    text="20",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

canvas.create_text(
    48.0,
    230.0,
    anchor="nw",
    text="10",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

canvas.create_text(
    132.0,
    137.0,
    anchor="nw",
    text="11:30",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

canvas.create_text(
    47.0,
    137.0,
    anchor="nw",
    text="20",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

canvas.create_text(
    107.0,
    200.0,
    anchor="nw",
    text="Recieved",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

canvas.create_text(
    139.0,
    115.0,
    anchor="nw",
    text="IST",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

canvas.create_text(
    12.0,
    115.0,
    anchor="nw",
    text="Mission(mins)",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

canvas.create_text(
    124.0,
    36.0,
    anchor="nw",
    text="DATA",
    fill="#FFFFFF",
    font=("Inter", 36 * -1)
)

canvas.create_text(
    47.0,
    92.0,
    anchor="nw",
    text="CLOCK",
    fill="#FFFFFF",
    font=("Inter", 20 * -1)
)



canvas.create_rectangle(
    1387.0,
    33.0,
    1915.0,
    351.0,
    fill="#0A0A0A",
    outline="")

canvas.create_rectangle(
    4.0,
    663.0,
    1915.0,
    1053.0,
    fill="#000000",
    outline="")


canvas.create_rectangle(
    5.0,
    0.0,
    55.0,
    19.0,
    fill="#39738B",
    outline="")



canvas.create_text(
    21.0,
    524.0,
    anchor="nw",
    text="Flight State",
    fill="#FFFFFF",
    font=("Inter", 36 * -1)
)

canvas.create_rectangle(
    227.0,
    537.0,
    248.0,
    556.0,
    fill="#000000",
    outline="")



canvas.create_text(
    613.0,
    31.0,
    anchor="nw",
    text="Port Settings",
    fill="#FFFFFF",
    font=("Inter", 36 * -1)
)

canvas.create_text(
    47.0,
    176.0,
    anchor="nw",
    text="Packets",
    fill="#FFFFFF",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    12.0,
    200.0,
    anchor="nw",
    text="Transmitted",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)

canvas.create_text(
    15.0,
    264.0,
    anchor="nw",
    text="No. of satelites :",
    fill="#FFFFFF",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    237.0,
    92.0,
    anchor="nw",
    text="Battery",
    fill="#FFFFFF",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    195.0,
    168.0,
    anchor="nw",
    text="Battery percentage",
    fill="#FFFFFF",
    font=("Inter", 15 * -1)
)


canvas.create_text(
    31.0,
    584.0,
    anchor="nw",
    text="Flight",
    fill="#FFFFFF",
    font=("Inter", 20 * -1)
)

canvas.create_text(
    500.0,
    248.0,
    anchor="nw",
    text="2022ASI-011",
    fill="#3D7B8A",
    font=("Inter", 36 * -1)
)
com_port_options = ["COM1", "COM2", "COM3", "COM4", "COM5"]
baud_rate_options = ["9600", "115200"]

com_port_var = tk.StringVar(window)
com_port_var.set(com_port_options[0])
com_port_menu = tk.OptionMenu(window, com_port_var, *com_port_options)
com_port_menu.place(x=697, y=129)
com_port_menu.config(
    width=9,
    height=1,
    bg="grey",
    fg="black",
    font=("Arial", 12),
)

baud_rate_var = tk.StringVar(window)
baud_rate_var.set(baud_rate_options[0])
baud_rate_menu = tk.OptionMenu(window, baud_rate_var, *baud_rate_options)
baud_rate_menu.place(x=697, y=168)
baud_rate_menu.config(
    width=9,
    height=1,
    bg="grey",
    fg="black",
    font=("Arial", 12),
)

serial_data_var = tk.StringVar()
serial_data_label = tk.Label(window, textvariable=serial_data_var, font=("Arial", 12))
serial_data_label.place(x=900,y=96)

altitude_label = tk.Label(window, text="Altitude: N/A", font=("Inter", 16), fg="white", bg="#000000")
altitude_label.place(x=14, y=414)

temperature_label = tk.Label(window, text="Temperature: N/A", font=("Inter", 16), fg="white", bg="#000000")
temperature_label.place(x=14, y=322)

pressure_label = tk.Label(window, text="Pressure: N/A", font=("Inter", 16), fg="white", bg="#000000")
pressure_label.place(x=14, y=352)


# image_label = tk.Label(window, image=img, bg="black", width=200, height=200)
# image_label.place(x=350, y=32)

canvas = FigureCanvasTkAgg(fig, master=window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.place(x=20, y=663, width=600, height=380)

canvas = FigureCanvasTkAgg(fig_1, master=window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.place(x=780, y=250, width=600, height=380)

canvas = FigureCanvasTkAgg(fig_acc, master=window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.place(x=1321, y=250, width=600, height=380)

canvas = FigureCanvasTkAgg(fig_p, master=window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.place(x=1315, y=663, width=600, height=380)

canvas = FigureCanvasTkAgg(fig_t, master=window)
canvas_widget = canvas.get_tk_widget()
canvas_widget.place(x=620, y=663, width=600, height=380)


start_button = tk.Button(window, text="Start", command=button,font=("Inter",14),bg="black",fg="white",width=15,height=2)
start_button.place(x=384, y=300)

stop_button = tk.Button(window, text="Stop", command=stop_animation,font=("Inter",14),bg="black",fg="white",width=15,height=2)
stop_button.place(x=384, y=400)

csv_button = tk.Button(window, text="Export", command=export_to_csv,font=("Inter",14),bg="black",fg="white",width=15,height=2)
csv_button.place(x=384, y=500)




window.mainloop()
ser.close()