set outputDir ./synth_out
set partName xcku5p-ffvb676-2-e
file mkdir $outputDir
read_verilog [glob ./src/hw/*.sv]
read_xdc ./src/hw/and_xor.xdc
synth_design -top and_xor -part $partName

write_checkpoint -force $outputDir/post_synth.dcp
report_utilization -file $outputDir/post_synth_util.rpt
report_timing_summary -file $outputDir/post_synth_timing.rpt
report_design_analysis -file $outputDir/post_synth_design_analysis.rpt
