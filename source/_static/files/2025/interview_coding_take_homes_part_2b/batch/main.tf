module "naming" {
    for_each = var.resources
    source = "../naming"

    base_name = each.key
    resource_type = each.value
}
