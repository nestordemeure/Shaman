
# SHAMANIZER : a python3 program that makes any C++ code src compatible
#
# work on a given file or on all the .c/.cpp/.h/.hpp in a given folder
# for each source file if it contains float/double/long double
#   replace the types
#   load src.h at the begining of the file
#   if it contains a printf
#       replace printf with tfm::printf
#       load tinyformat.h at the begining of the file (https://github.com/c42f/tinyformat)
#   deals with MPI
#   deals with Eigen

# SHAMAN
shamanHeader = "#include <src/Shaman.h>"
numericTypes = [("float","Sfloat"), ("double","Sdouble"), ("long double","Slong_double")]
cpp_extensions = (".h", ".c", ".cpp", ".hpp", ".cc", ".cxx", ".c++", ".hh", ".hxx", ".h++") # tuple required

# STANDARD LIBRARY
printfHeader = "#include <shamanizer/tinyformat.h>"
printfFunctions = [("printf","tfm::printf")] # TODO add a warning for 'fprintf'
stdFunctions = ['abs','labs','llabs','div','ldiv','lldiv','imaxabs','imaxdiv','fabs',
                'fmod','remainder','remquo','fma','fmax','fmin','fdim','exp','exp2','expm1','log','log10','log2','log1p',
                'pow','sqrt','cbrt','hypot','sin','cos','tan','asin','acos','atan','atan2','sinh','cosh','tanh','asinh','acosh','atanh',
                'erf','erfc','tgamma','lgamma','ceil','floor','trunc','round','lround','llround','nearbyint','rint','lrint','llrint',
                'frexp','ldexp','modf','scalbn','scalbln','ilogb','logb','nextafter','nexttoward','copysign','fpclassify',
                'isfinite','isinf','isnan','isnormal','signbit','isgreater','isgreaterequal','isless','islessequal','islessgreater','isunordered']

# MPI
mpiHeader = "#include <src/Shaman_mpi.h>"
mpiTypes = [("MPI_FLOAT","MPI_SFLOAT"), ("MPI_DOUBLE","MPI_SDOUBLE"), ("MPI_LONG_DOUBLE","MPI_SLONG_DOUBLE")]
mpiOperations = [("MPI_MAX","MPI_SMAX"), ("MPI_MIN","MPI_SMIN"), ("MPI_SUM","MPI_SSUM"), ("MPI_PROD","MPI_SPROD")]
mpiFunctions = [("MPI_Init","MPI_Shaman_Init"), ("MPI_Finalize","MPI_Shaman_Finalize")]

# EIGEN
eigenHeader = "#include <src/Shaman_eigen.h>"
eigenMatrixTypes = [("Matrix2cd","SMatrix2cd"), ("Matrix2cf","SMatrix2cf"), ("Matrix2d","SMatrix2d"), ("Matrix2f","SMatrix2f"),("Matrix2Xcd","SMatrix2Xcd"),
              ("Matrix2Xcf","SMatrix2Xcf"), ("Matrix3cd","SMatrix3cd"), ("Matrix3cf","SMatrix3cf"), ("Matrix3d","SMatrix3d"), ("Matrix3f","SMatrix3f"),
              ("Matrix2Xd","SMatrix2Xd"), ("Matrix2Xf","SMatrix2Xf"), ("Matrix3Xcd","SMatrix3Xcd"), ("Matrix3Xcf","SMatrix3Xcf"), ("Matrix3Xd","SMatrix3Xd"),
              ("Matrix3Xf","SMatrix3Xf"), ("Matrix4cd","SMatrix4cd"), ("Matrix4cf","SMatrix4cf"), ("Matrix4d","SMatrix4d"), ("Matrix4f","SMatrix4f"),
              ("Matrix4Xcd","SMatrix4Xcd"), ("Matrix4Xcf","SMatrix4Xcf"), ("Matrix4Xd","SMatrix4Xd"), ("Matrix4Xf","SMatrix4Xf"), ("MatrixX2cd","SMatrixX2cd"),
              ("MatrixX2cf","SMatrixX2cf"), ("MatrixX2d","SMatrixX2d"), ("MatrixX2f","SMatrixX2f"), ("MatrixX3cd","SMatrixX3cd"), ("MatrixX3cf","SMatrixX3cf"),
              ("MatrixX3d","SMatrixX3d"), ("MatrixX3f","SMatrixX3f"), ("MatrixX4cd","SMatrixX4cd"), ("MatrixX4cf","SMatrixX4cf"), ("MatrixX4d","SMatrixX4d"),
              ("MatrixX4f","SMatrixX4f"), ("MatrixXcd","SMatrixXcd"), ("MatrixXcf","SMatrixXcf"), ("MatrixXd","SMatrixXd"), ("MatrixXf","SMatrixXf"),
              ("RowVector2cd","SRowVector2cd"), ("RowVector2cf","SRowVector2cf"), ("RowVector2d","SRowVector2d"), ("RowVector2f","SRowVector2f"),
              ("RowVector3cd","SRowVector3cd"), ("RowVector3cf","SRowVector3cf"), ("RowVector3d","SRowVector3d"), ("RowVector3f","SRowVector3f"),
              ("RowVector4cd","SRowVector4cd"), ("RowVector4cf","SRowVector4cf"), ("RowVector4d","SRowVector4d"), ("RowVector4f","SRowVector4f"),
              ("RowVectorXcd","SRowVectorXcd"), ("RowVectorXcf","SRowVectorXcf"), ("RowVectorXd","SRowVectorXd"), ("RowVectorXf","SRowVectorXf"),
              ("Vector2cd","SVector2cd"), ("Vector2cf","SVector2cf"), ("Vector2d","SVector2d"), ("Vector2f","SVector2f"), ("Vector3cd","SVector3cd"),
              ("Vector3cf","SVector3cf"), ("Vector3d","SVector3d"), ("Vector3f","SVector3f"), ("Vector4cd","SVector4cd"), ("Vector4cf","SVector4cf"),
              ("Vector4d","SVector4d"), ("Vector4f","SVector4f"), ("VectorXcd","SVectorXcd"), ("VectorXcf","SVectorXcf"), ("VectorXd","SVectorXd"),
              ("VectorXf","SVectorXf")]
eigenArrayTypes = [("ArrayXXf","SArrayXXf"), ("ArrayXd","SArrayXd"), ("Array33f","SArray33f"), ("Array4f","SArray4f")]
eigenTypes = eigenMatrixTypes + eigenArrayTypes

#-----------------------------------------------------------------------------
# MODIFICATION COUNT

# dictionary that contains a default value (0) for easy increment
from collections import defaultdict

# used to store the number and nature of modifications done to the code
modification_counter = defaultdict(int)

def display_modification_summary():
    """displays the modifications done to the code"""
    if len(modification_counter) == 0:
        print("Nothing was changed.")
    for k,v in modification_counter.items():
        print(v, k, "have been replaced", sep=' ')

#-----------------------------------------------------------------------------
# STRING OPERATIONS

import re

def replace_strings_in_line(strings, line):
    """returns none (if no actions were available) or some newline if it was able to apply some string replacement"""
    changed = False
    for oldString,newString in strings:
        # does not match a pattern that is stuck to an alphanumeric character ('float1' would not match for 'float' but '[float]' would)
        line, matchnumber = re.subn('(^|\W)' + oldString + '(\W|$)', '\g<1>' + newString + '\g<2>', line)
        if matchnumber > 0:
            changed = True
            modification_counter[oldString] += matchnumber
    return line if changed else None

def replace_strings_in_text(strings, lines):
    """returns none (if no actions were available) or some lines if it was able to apply some string replacement"""
    changed = False
    for i,line in enumerate(lines):
        newline = replace_strings_in_line(strings, line)
        if newline is not None:
            changed = True
            lines[i] = newline
    return lines if changed else None

#-----------------------------------------------------------------------------
# WARNING

def contains_string(string,lines):
    """returns true if at least one of the lines contains the given string"""
    for line in lines:
        if string in line:
            return True
    return False

def std_functions_warning(filepath, lines):
    """if contains stdFunction then warning with function name and file name"""
    for functionName in stdFunctions:
        if contains_string("std::" + functionName, lines):
            print("WARNING : std::" + functionName + " found in '" + filepath + "', you might want to replace it with the equivalent src function.")

#-----------------------------------------------------------------------------
# HEADER

def find_header_index(lines):
    """returns a position to insert an header into a file (just before the first header, if it exists, or on the first line)"""
    for i,line in enumerate(lines):
        if line.startswith("#include"):
            return i
    return 0

def add_header(header, lines):
    """adds a given header in the lines"""
    lines.insert(find_header_index(lines), header + '\n')

#-----------------------------------------------------------------------------
# CODE REWRITING

import os

def export_lines(filepath,lines):
    """exports the lines to a renammed file"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as newfile:
        newfile.writelines(lines)

def change_printf(filepath, lines):
    """modifies the printf if needed and exports the lines"""
    newlines = replace_strings_in_text(printfFunctions, lines)
    if newlines is not None:
        add_header(printfHeader, newlines)
        print("WARNING : 'printf' found in '" + filepath + "', don't forget to compile with the 'tinyformat' library.")
        export_lines(filepath, newlines)
    else:
        export_lines(filepath, lines)

def change_mpi(filepath, lines):
    """modifies the MPI calls if needed and exports the lines"""
    newlines = replace_strings_in_text(mpiTypes + mpiOperations + mpiFunctions, lines)
    if newlines is not None:
        add_header(mpiHeader, newlines)
        print("WARNING : MPI functions found in '" + filepath + "', don't forget to compile with the 'Shaman_mpi.h' file.")
        change_printf(filepath, newlines)
    else:
        change_printf(filepath, lines)

def change_eigen(filepath, lines):
    """modifies the Eigen types if needed and exports the lines"""
    newlines = replace_strings_in_text(eigenTypes, lines)
    if newlines is not None:
        add_header(eigenHeader, newlines)
        print("WARNING : eigen types found in '" + filepath + "', don't forget to compile with the 'Shaman_eigen.h' file.")
        change_mpi(filepath, newlines)
    else:
        change_mpi(filepath, lines)

def change_type(filepath, lines):
    """if needed, modifies the types and forward to the printf"""
    newlines = replace_strings_in_text(numericTypes, lines)
    if newlines is not None:
        std_functions_warning(filepath, lines)
        add_header(shamanHeader, newlines)
        change_eigen(filepath, newlines)
    else:
        export_lines(filepath, lines)

#-----------------------------------------------------------------------------
# SHAMANIZER

from sys import argv

def list_cpp_files(rootpath):
    """list the cpp files associated with the given path"""
    if os.path.isfile(rootpath):
        if not rootpath.endswith(cpp_extensions) : print("WARNING : '", rootpath, "' does not end with a known C++ extension.")
        yield rootpath
    else:
        for file in os.scandir(rootpath):
           if file.is_file() and file.name.endswith(cpp_extensions):
              yield file.path
           elif file.is_dir():
              yield from list_cpp_files(file.path)
    # Older version that does not go in subdirectories
    #if not os.path.isfile(rootpath):
    #    return [file.path for file in os.scandir(rootpath) if file.is_file() and file.name.endswith(cpp_extensions)]
    #else:
    #    if not rootpath.endswith(cpp_extensions) :
    #        print("WARNING : '", rootpath, "' does not end with a known C++ extension.")
    #    return [rootpath]

def shamanize_name(rootpath,filepath):
    """adds the src prefix to a path produce from a root"""
    prefixpath, targetname = os.path.split(rootpath)
    shamanpath = prefixpath + '/' +  "shaman_" + targetname
    return filepath.replace(rootpath,shamanpath)

def shamanize_file(filepath, outpath):
    """deals with types, printf and code exportation"""
    with open(filepath, 'r') as file:
        lines = file.readlines()
        change_type(outpath, lines)

def shamanizer(path):
    """takes a path and addapt all associated files to Shaman"""
    print("*** SHAMANIZER ***")
    for filepath in list_cpp_files(path):
        outpath = shamanize_name(path,filepath)
        shamanize_file(filepath, outpath)
    display_modification_summary()

#-----------------------------------------------------------------------------
# MAIN

# applies shamanizer to all the arguments in path
path_list = argv[1:] # skip the name of the program
for rootpath in path_list:
    shamanizer(rootpath)

# TODO might run on all single files when given a folder with a path that ends with '/'

