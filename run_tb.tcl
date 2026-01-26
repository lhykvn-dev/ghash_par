# vivado -mode batch -source run_tb.tcl
# vivado -mode gui -source run_rb.tcl

set project_name "tb_sim"
set top_module "tb"
set output_dir "./tb_output"
file mkdir $output_dir
create_project -force $project_name $output_dir -part xcku5p-ffvb676-2-e
add_files -norecurse {
    ./src/hw/and_xor.sv
    ./src/hw/tb/tb.sv
}

update_compile_order -fileset sources_1
set_property top $top_module [get_filesets sim_1]
launch_simulation -simset [get_filesets sim_1] -mode behavioral
# open_wave_config # GUI mode
# run all
close_project