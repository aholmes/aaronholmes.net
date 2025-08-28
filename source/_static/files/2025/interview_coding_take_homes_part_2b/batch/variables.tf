variable "resources" {
    description = "A map of base names and resource types."
    type = map(string) # {"app":"virtual_machine", "data":"storage_account", ...}
}
