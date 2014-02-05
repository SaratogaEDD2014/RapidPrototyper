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

def test1(process_function):
    #define test conditions and headers
    header_row = 1
    data_row = header_row + 1
    test_path = 'C:/Users/Robert Krulcik/Documents/GitHub/EfficiencyTesting/'
    name = 'test_one_'
    base_names = [('test_one_'+ str(i)+'.stl') for i in range(7)]
    num_teeth  = [10, 20, 40, 80, 160, 320, 640]
    num_facets = numpy.array(num_teeth)*56
    header_columns = ['Name', 'Num Teeth', 'Num Facets', 'Process Time']

    #Set up spreadsheet
    gc = gspread.login('skrulcik@gmail.com', 'cvzaijcyqyexknlf')
    doc = gc.open("ProfileSTL")
    wks = doc.worksheet('TestA')

    #Fill in headers
    for i in range(len(header_columns)):
        wks.update_cell(header_row, i+1, header_columns[i])   #i+1 is because there is no '0' in spreadsheet
    #Fill in data
    for i in range(len(base_names)):
        try:
            start_time = time.time()
            process_function(test_path + base_names[i])
            process_time = str(time.time() - start_time) + "seconds"
        except e:
            process_time = 'Error: '+e
        wks.update_cell(data_row, 1, base_names[i])
        wks.update_cell(data_row, 2, num_teeth[i])
        wks.update_cell(data_row, 3, num_facets[i])
        wks.update_cell(data_row, 4, process_time)
        data_row += 1

if __name__ == '__main__':
    app = wx.App()
    test1(parser.process_file)
    app.MainLoop()