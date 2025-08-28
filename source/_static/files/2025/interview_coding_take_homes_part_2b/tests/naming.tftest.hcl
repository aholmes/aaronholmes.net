run "resource_type_can_be_virtual_machine" {
    command = plan
    module {
        source = "./naming"
    }

    variables {
        base_name = "foo"
        resource_type = "virtual_machine"
    }

    assert {
        condition = output.resource_name == "vm-foo-00"
        error_message = "VM name is wrong"
    }
}

run "resource_type_can_be_storage_account" {
    command = plan
    module {
        source = "./naming"
    }

    variables {
        base_name = "foo"
        resource_type = "storage_account"
    }

    assert {
        condition = output.resource_name == "safoo"
        error_message = "Storage name is wrong"
    }
}

run "resource_type_can_be_key_vault" {
    command = plan
    module {
        source = "./naming"
    }

    variables {
        base_name = "foo"
        resource_type = "key_vault"
    }

    assert {
        condition = output.resource_name == "kv-foo"
        error_message = "Key vault name is wrong"
    }
}

run "resource_type_errors_when_invalid" {
    command = plan
    module {
        source = "./naming"
    }

    variables {
        base_name = "foo"
        resource_type = "lambda"
    }

    expect_failures = [
        var.resource_type,
    ]
}

run "long_vm_name_is_truncated" {
    command = plan
    module {
        source = "./naming"
    }

    variables {
        base_name = "fooBARbaz-FOObarBAZ"
        resource_type = "virtual_machine"
    }

    assert {
        condition = output.resource_name == "vm-fooBARbaz-00"
        error_message = "VM name is wrong"
    }
}

run "short_vm_name_is_unmodified" {
    command = plan
    module {
        source = "./naming"
    }

    variables {
        base_name = "foo"
        resource_type = "virtual_machine"
    }

    assert {
        condition = output.resource_name == "vm-foo-00"
        error_message = "VM name is wrong"
    }
}

run "storage_account_is_lower_and_no_dashes" {
    command = plan
    module {
        source = "./naming"
    }

    variables {
        base_name = "data-DATA-data-DATA-data"
        resource_type = "storage_account"
    }

    assert {
        condition = output.resource_name == "sadatadatadatadatadata"
        error_message = "Store name is wrong"
    }
}

run "keyvault_is_lower" {
    command = plan
    module {
        source = "./naming"
    }

    variables {
        base_name = "secretsSECRETS-secretsSECRETS"
        resource_type = "key_vault"
    }

    assert {
        condition = output.resource_name == "kv-secretssecrets-secretssecrets"
        error_message = "Key vault name is wrong"
    }
}
