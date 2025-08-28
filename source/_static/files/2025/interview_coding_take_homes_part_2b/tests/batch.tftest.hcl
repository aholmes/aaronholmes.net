run "long_vm_name_is_truncated" {
    command = plan
    module {
        source = "./batch"
    }

    variables {
        resources = {
            "fooBARbaz-FOObarBAZ" = "virtual_machine"
        }
    }

    assert {
        condition = output.resource_names["fooBARbaz-FOObarBAZ"] == "vm-fooBARbaz-00"
        error_message = "VM name is wrong"
    }
}

run "short_vm_name_is_unmodified" {
    command = plan
    module {
        source = "./batch"
    }

    variables {
        resources = {
            "foo" = "virtual_machine"
        }
    }

    assert {
        condition = output.resource_names["foo"] == "vm-foo-00"
        error_message = "VM name is wrong"
    }
}

run "storage_account_is_lower_and_no_dashes" {
    command = plan
    module {
        source = "./batch"
    }

    variables {
        resources = {
            "data-DATA-data-DATA-data" = "storage_account"
        }
    }

    assert {
        condition = output.resource_names["data-DATA-data-DATA-data"] == "sadatadatadatadatadata"
        error_message = "Store name is wrong"
    }
}

run "keyvault_is_lower" {
    command = plan
    module {
        source = "./batch"
    }

    variables {
        resources = {
            "secretsSECRETS-secretsSECRETS" = "key_vault"
        }
    }

    assert {
        condition = output.resource_names["secretsSECRETS-secretsSECRETS"] == "kv-secretssecrets-secretssecrets"
        error_message = "Key vault name is wrong"
    }
}
