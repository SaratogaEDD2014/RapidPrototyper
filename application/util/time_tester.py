##TEST 1: NUMBER OF FACETS
##    Gear Dimensions:
##        bore diameter: 1.0
##        number of teeth: [6, 12, 18, 24, 30, 36, 42]
##        pitch diameter: 3.0
##        tooth shape: trapezoid
##        thickness: .25
##
##        hub diameter: 0.0
##        hub thickness: 0.0
##
##TEST 2: THICKNESS TEST
##    Gear Dimensions:
##        bore diameter: 1.0
##        number of teeth: 16
##        pitch diameter: 3.0
##        tooth shape: trapezoid
##        thickness:[.2, .4, .6, .8, 1., 1.2, 1.4]
##
##        hub diameter: 2.0
##        hub thickness: [.2, .4, .6, .8, 1., 1.2, 1.4]
import wx
import time
import gspread
import numpy
import application.util.stl_to_bitmap as parser
import application.settings as settings

#FOR TESTING: app hasn't started so path in stl_to_bitmap is invalid
parser.BITMAP_DIR = 'C:/Users/Robert Krulcik/Documents/GitHub\RapidPrototyper/GUI/generation_buffer/'

def test1(process_function, test_designation):
    #define test conditions and headers
    header_row = 1
    data_row = header_row + 1
    test_path = 'C:/Users/Robert Krulcik/Documents/GitHub/EfficiencyTesting/'
    name = 'test_one_'
    designation = test_designation
    num_teeth  = [6, 12, 18, 24, 30, 36, 42]
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
            num_facets = process_function(test_path + base_names[i])
            process_time = str(time.time() - start_time)
        except Exception, e:
            print 'failed',e
            num_facets = 0
            process_time = 'Error: Could not time, program failed.'
        wks.update_cell(data_row, 1, base_names[i])
        wks.update_cell(data_row, 2, num_teeth[i])
        wks.update_cell(data_row, 3, num_facets)
        wks.update_cell(data_row, 4, process_time)
        data_row += 1
    wks.update_cell(data_row, 1, "Seconds per facet:")
    start_facets = as_alpha(3) + str(header_row+1)
    end_facets = as_alpha(3) + str(data_row-1)
    start_seconds = as_alpha(4) + str(header_row+1)
    end_seconds = as_alpha(4) + str(data_row-1)
    wks.update_cell(data_row, 2, "=SUM("+start_seconds+":"+end_seconds+")/SUM("+start_facets+":"+end_facets+")")

def test2(process_function, test_designation):
    #define test conditions and headers
    header_row = 12
    data_row = header_row + 1
    test_path = 'C:/Users/Robert Krulcik/Documents/GitHub/EfficiencyTesting/'
    name = 'test_two_'
    designation = test_designation
    thickness  = [.2, .4, .6, .8, 1., 1.2, 1.4]
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
        except Exception, e:
            print e
            process_time = 'Error: Could not time, program failed.'
        wks.update_cell(data_row, 1, base_names[i])
        total_thickness = (thickness[i] + hub_thickness[i])
        wks.update_cell(data_row, 2, total_thickness)
        num_layers = round(total_thickness/settings.LAYER_DEPTH)
        wks.update_cell(data_row, 3, num_layers)
        wks.update_cell(data_row, 4, process_time)
        data_row += 1
    wks.update_cell(data_row, 1, "Seconds per layer:")
    start_layer = as_alpha(3) + str(header_row+1)
    end_layer = as_alpha(3) + str(data_row-1)
    start_seconds = as_alpha(4) + str(header_row+1)
    end_seconds = as_alpha(4) + str(data_row-1)
    wks.update_cell(data_row, 2, "=SUM("+start_seconds+":"+end_seconds+")/SUM("+start_layer+":"+end_layer+")")

def profile_only(process_function):
    import cProfile
    #define test conditions and headers
    header_row = 12
    data_row = header_row + 1
    test_path = 'C:/Users/Robert Krulcik/Documents/GitHub/EfficiencyTesting/'
    name = 'test_two_'
    thickness  = [.2, .4, .6, .8, 1., 1.2, 1.4]
    hub_thickness = thickness[:]
    base_names = [(name+str(i)+'.stl') for i in range(len(thickness))]

    #Fill in data
    for i in range(len(base_names)):
        try:
            name = 'parser.process_file("'+ test_path + str(base_names[i]) +'")'
            print name
            cProfile.run(name)
        except Exception, e:
            print e
            process_time = 'Error: Could not time, program failed.'
        total_thickness = (thickness[i] + hub_thickness[i])
        num_layers = round(total_thickness/settings.LAYER_DEPTH)
        print "Total thickness: ", total_thickness
        print "Number of layers: ", num_layers

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


revision = 'C'
if __name__ == '__main__':
    app = wx.App()
    #test1(parser.process_file, 'Test'+revision)
    #test2(parser.process_file, 'Test'+revision)
    profile_only(parser.process_file)
    app.MainLoop()