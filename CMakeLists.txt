cmake_minimum_required(VERSION 3.15)
project(Firmware_Master_Project C)

find_package(Python3 REQUIRED COMPONENTS Interpreter)

option(ENABLE_MISRA_EXECUTION "Run AbsInt a3 after generating DAX files" OFF)

# CMAKE PYTHON BRIDGE FUNCTION
function(add_misra_target MODULE_NAME SOURCES_VAR INCLUDES_VAR OUTPUT_DIR)
    if(ENABLE_MISRA_EXECUTION)
        set(EXECUTE_FLAG "--run")
    else()
        set(EXECUTE_FLAG "")
    endif()

    add_custom_target(misra_${MODULE_NAME} ALL
        COMMAND Python3::Interpreter "${CMAKE_SOURCE_DIR}/static_analysis/cmake_dax_gen.py"
            --module "${MODULE_NAME}"
            --sources ${${SOURCES_VAR}}     
            --includes ${${INCLUDES_VAR}}
            --out-dir "${OUTPUT_DIR}"       
            ${EXECUTE_FLAG}            
        WORKING_DIRECTORY "${CMAKE_BINARY_DIR}"
        COMMENT "Starting MISRA static analysis for ${MODULE_NAME}..."
        VERBATIM
    )

    if(NOT TARGET misra_analyze_all)
        add_custom_target(misra_analyze_all COMMENT "Running all MISRA checks...")
    endif()
    add_dependencies(misra_analyze_all misra_${MODULE_NAME})

endfunction()

#Module 1 :-
set(MAIN 
    "${CMAKE_CURRENT_SOURCE_DIR}/source/src/main.c" #Source File Paths
)
set(MAIN_INC 
    "${CMAKE_CURRENT_SOURCE_DIR}/source/include"  #Include File Paths
)

set(MAIN_DST "${CMAKE_CURRENT_SOURCE_DIR}/SA_Reports/main") #Destination Path for .dax file and reports folder

add_misra_target("MAIN" MAIN MAIN_INC "${MAIN_DST}") #Function call to python

#Module 2 :-
set(GEN 
    "${CMAKE_CURRENT_SOURCE_DIR}/gen/gen.c" #Source File Paths
)
set(GEN_INC 
    "${CMAKE_CURRENT_SOURCE_DIR}/gen"  #Include File Paths
)

set(GEN_DST "${CMAKE_CURRENT_SOURCE_DIR}/SA_Reports/gen") #Destination Path for .dax file and reports folder

add_misra_target("GEN" GEN GEN_INC "${GEN_DST}") #Function call to python