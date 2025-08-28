# example usage
module "batch" {
    source = "./batch"
    resources = {
        "fooBARbaz-FOObarBAZ" = "virtual_machine",
        "appappappappappappappappapp" = "virtual_machine",
        "data-DATA-data-DATA-data" = "storage_account",
        "otherdata" = "storage_account",
        "secretsSECRETSsecretsSECRETS" = "key_vault",
        "othersecrets" = "key_vault"
        "VERY-long-virtual-machine-name" = "virtual_machine",
        "CrAzY-Kv-NaMe" = "key_vault",
        "CrAzY-Sa-NaMe" = "storage_account"
    }
}
