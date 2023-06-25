def parse_imu_data(data : bytearray, dof : int) -> tuple:
    data_string = data.decode('utf-8')
    
    end_delimeter = '#'
    data_delimeter = ','
    
    data_string = data_string.split(end_delimeter)[0]
    values = [float(x) for x in data_string.split(',')]

    # [0, 2] aceleroscope data, [3,5] gyroscope data, magnetoscope data [6,8]
    if dof == 9:
        return values[:3], values[3:6], values[6:]
    if dof == 6:
        return values[:3], values[3:], []


