locals {
    base_name = (
        var.resource_type == "virtual_machine" ? substr(var.base_name, 0, 15 - length("vm-") - length("-00")) :
        var.resource_type == "key_vault" ? lower(var.base_name) :
        lower(replace(var.base_name, "-", "")) # storage account
    )

    resource_name = (
        var.resource_type == "virtual_machine" ? "vm-${local.base_name}-00" :
        var.resource_type == "key_vault" ? "kv-${local.base_name}" :
        "sa${local.base_name}" # storage account
    )
}
