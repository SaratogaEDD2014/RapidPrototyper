##TEST 1: NUMBER OF FACETS
##    Gear Dimensions:
##        bore diameter: 1.0
##        number of teeth: [10, 20, 40, 80, 160, 320, 640]
##        pitch diameter: 3.0
##        tooth shape: trapezoid
##        thickness: .25
##
##        hub diameter: 2.0
##        hub thickness: .25
##
##TEST 2: THICKNESS TEST
##    Gear Dimensions:
##        bore diameter: 1.0
##        number of teeth: 16
##        pitch diameter: 3.0
##        tooth shape: trapezoid
##        thickness: [1, 2, 3, 4, 5, 6, 7]
##
##        hub diameter: 2.0
##        hub thickness: [1, 2, 3, 4, 5, 6, 7]
import wx
import time
import gspread
import numpy
import GUI.util.stl_to_bitmap as parser
import GUI.settings

def test1(process_function):
    #define test conditions and headers
    header_row = 1
    data_row = header_row + 1
    test_path = 'C:/Users/Robert Krulcik/Documents/GitHub/EfficiencyTesting/'
    name = 'test_one_'
    designation = 'TestA'
    num_teeth  = [10, 20, 40, 80, 160, 320]
    num_facets = numpy.array(num_teeth)*56
    base_names = [(name+str(i)+'.stl') for i in range(len(num_teeth))]
    header_columns = ['Name', 'Num Teeth', 'Num Facets', designation]

    #Set up spreadsheet
    gc = gspread.login('skrulcik@gmail.com', 'cvzaijcyqyexknlf')
    doc = gc.open("ProfileSTL")
    try:
        wks = doc.worksheet(designation)
    except:
        wks = doc.add_worksheet(designation, 100,50)

    #Fill in headers
    for i in range(len(header_columns)):
        wks.update_cell(header_row, i+1, header_columns[i])   #i+1 is because there is no '0' in spreadsheet
    #Fill in data
    for i in range(len(base_names)):
        try:
            start_time = time.time()
            process_function(test_path + base_names[i])
            process_time = str(time.time() - start_time)
        except:
            process_time = 'Error: Could not time, program failed.'
        wks.update_cell(data_row, 1, base_names[i])
        wks.update_cell(data_row, 2, num_teeth[i])
        wks.update_cell(data_row, 3, num_facets[i])
        wks.update_cell(data_row, 4, process_time)
        data_row += 1
    wks.update_cell(data_row, 1, "Seconds per facet:")
    start_facets = as_alpha(3) + str(header_row+1)
    end_facets = as_alpha(3) + str(data_row-1)
    start_seconds = as_alpha(4) + str(header_row+1)
    end_seconds = as_alpha(4) + str(data_row-1)
    wks.update_cell(data_row, 2, "=SUM("+start_seconds+":"+end_seconds+")/SUM("+start_facets+":"+end_facets+")")

def test2(process_function):
    #define test conditions and headers
    header_row = 12
    data_row = header_row + 1
    test_path = 'C:/Users/Robert Krulcik/Documents/GitHub/EfficiencyTesting/'
    name = 'test_two_'
    designation = 'TestA'
    thickness  = [1, 2, 3, 4, 5, 6, 7]
    hub_thickness = thickness[:]
    base_names = [(name+str(i)+'.stl') for i in range(len(thickness))]
    header_columns = ['Name', 'Total Thickness (in.)', 'Num Layers', designation]
    
    #Set up spreadsheet
    gc = gspread.login('skrulcik@gmail.com', 'cvzaijcyqyexknlf')
    doc = gc.open("ProfileSTL")
    try:
        wks = doc.worksheet(designation)
    except:
        wks = doc.add_worksheet(designation, 100,50)
    
    #Fill in headers
    for i in range(len(header_columns)):
        wks.update_cell(header_row, i+1, header_columns[i])   #i+1 is because there is no '0' in spreadsheet
    #Fill in data
    for i in range(len(base_names)):
        try:
            start_time = time.time()
            process_function(test_path + base_names[i])
            process_time = str(time.time() - start_time)
        except:
            process_time = 'Error: Could not time, program failed.'
        wks.update_cell(data_row, 1, base_names[i])
        total_thickness = (thickness[i] + hub_thickness[i])
        wks.update_cell(data_row, 2, total_thickness)
        num_layers = total_thickness/settings.LAYER_DEPTH
        wks.update_cell(data_row, 3, num_layers)
        wks.update_cell(data_row, 4, process_time)
        data_row += 1
    wks.update_cell(data_row, 1, "Seconds per layer:")
    start_layer = as_alpha(3) + str(header_row+1)
    end_layer = as_alpha(3) + str(data_row-1)
    start_seconds = as_alpha(4) + str(header_row+1)
    end_seconds = as_alpha(4) + str(data_row-1)
    wks.update_cell(data_row, 2, "=SUM("+start_seconds+":"+end_seconds+")/SUM("+start_layer+":"+end_layer+")")

def as_alpha(index):
    index -= 1 #No 0 in spreadsheet, when they want A they give '1' but A is at index 0
    alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','Q','R','S','T','U','V','W','X','Y','Z']
    if index<len(alpha) and index>=0:
        return alpha[index]
    elif index>0:
        #Start 2 number designations
        i1 = (index/len(alpha))-1
        i2 = (index%len(alpha))
        return alpha[i1]+ alpha[i2]
    else:
        return alpha[0]



if __name__ == '__main__':
    app = wx.App()
    #test1(parser.process_file)
    test2(parser.process_file)
    app.MainLoop()