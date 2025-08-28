output "resource_names" {
    description = "A map of base names to formatted resource names."
    value = { for k, v in module.naming: k => v.resource_name }
}

output "all_naming_outputs" {
    value = module.naming
}
