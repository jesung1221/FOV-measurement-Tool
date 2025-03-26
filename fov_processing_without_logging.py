import math
import pandas as pd
from tkinter import messagebox, END

def calculate_fovs(width, height, distance):
    h_fov = math.degrees(2 * math.atan((width / 2) / distance))
    v_fov = math.degrees(2 * math.atan((height / 2) / distance))
    d_fov = math.degrees(2 * math.atan(math.sqrt(width**2 + height**2) / 2 / distance))
    
    return h_fov, v_fov, d_fov

def process_measurements(listbox, chart_169_width, chart_169_height, chart_43_width, chart_43_height):
    data = []
    measurements = listbox.get(0, END)

    for measurement in measurements:
        parts = measurement.split('_')
        device = parts[0].upper()  # Normalize to uppercase
        camera = parts[1]
        mode = parts[2]
        resolution = parts[3]
        aspect_ratio = parts[4]
        distance = float(parts[5])  # Attempt to convert distance to float
        
        if aspect_ratio == "16:9":
            width = float(chart_169_width.get())
            height = float(chart_169_height.get())
        else:
            width = float(chart_43_width.get())
            height = float(chart_43_height.get())
        
        h_fov, v_fov, d_fov = calculate_fovs(width, height, distance)
        
        # Append data to list, including the aspect ratio
        data.append([device, camera, mode, resolution, aspect_ratio, distance, h_fov, v_fov, d_fov])
    
    # Create a DataFrame from the data
    df = pd.DataFrame(data, columns=["Device", "Camera", "Mode", "Resolution", "Aspect Ratio", "Distance to the chart (cm)", "Horizontal FOV (deg)", "Vertical FOV (deg)", "Diagonal FOV (deg)"])
    
    # Sort the DataFrame by the "Device" column
    df.sort_values(by="Device", inplace=True)
    
    # Try saving the DataFrame to Excel
    try:
        with pd.ExcelWriter("FOV_Measurements.xlsx", engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="FOV Data")
            
            # Add chart size information in the same Excel file
            chart_info = pd.DataFrame({
                "Aspect Ratio": ["16:9", "4:3"],
                "Width (cm)": [chart_169_width.get(), chart_43_width.get()],
                "Height (cm)": [chart_169_height.get(), chart_43_height.get()]
            })
            chart_info.to_excel(writer, index=False, sheet_name="Chart Size Info")
            
            # Auto-adjust column widths for "FOV Data"
            workbook = writer.book
            worksheet = writer.sheets["FOV Data"]
            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column[0].column_letter].width = adjusted_width
            
            # Auto-adjust column widths for "Chart Size Info"
            worksheet = writer.sheets["Chart Size Info"]
            for column in worksheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column[0].column_letter].width = adjusted_width

        # Inform the user that the Excel file has been created successfully
        messagebox.showinfo("Success", "Excel file 'FOV_Measurements.xlsx' has been created successfully.")
    
    except PermissionError:
        messagebox.showerror("File Error", "Permission denied: 'FOV_Measurements.xlsx'. Please close the Excel file if it is open and try again.")
