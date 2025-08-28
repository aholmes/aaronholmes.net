# these outputs are just to show what the modules are outputting.
output "resources" {
    value = module.batch.resource_names
}
output "all_naming_outputs" {
    value = module.batch.all_naming_outputs
}
