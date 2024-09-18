from json import dumps
import sys

data = {
    "BaseCommon": {
        "inherits": [],
        "properties": {
            "env": {
                "type": "Environment",
                "comment": "With disabled mail tracking"
            },
            "partner": {
                "type": "res.partner",
                "comment": "a new partner"
            },
            "currency": {
                "type": "res.currency",
                "comment": "company_id.currency_id"
            }
        }
    },
    "UomCommon": {
        "inherits": [],
        "properties": {
            "uom_gram": {
                "type": "uom.uom"
            },
            "uom_kgm": {
                "type": "uom.uom"
            },
            "uom_ton": {
                "type": "uom.uom"
            },
            "uom_unit": {
                "type": "uom.uom"
            },
            "uom_dozen": {
                "type": "uom.uom"
            },
            "group_uom": {
                "type": "res.groups",
                "comment": "Security group of uom access"
            }
        },
        "methods": {
            "_enable_uom": {
                "comment": "Enable uom group for current env's user"
            },
            "_disable_uom": {
                "comment": "Disable uom group for current env's user"
            }
        }
    },
    "ProductCommon": {
        "inherits": [
            "BaseCommon",
            "UomCommon"
        ],
        "does": "Set env's company currency to usd, disable all pricelists.",
        "properties": {
            "currency": {
                "type": "res.currency",
                "value": "USD",
                "comment": "overrides BaseCommon.currency, also sets it as company currency"
            },
            "product_category": {
                "type": "product.category",
                "comment": "a new category"
            },
            "product": {
                "type": "product.product",
                "comment": "a new consumable product, in cls.product_category"
            },
            "service_product": {
                "type": "product.product",
                "comment": "a new service product, in cls.product_category"
            },
            "consumable_product": {
                "type": "product.product",
                "comment": "pointer to cls.product"
            },
            "pricelist": {
                "type": "product.pricelist",
                "comment": "a new pricelist"
            }
        },
        "methods": {
            "_archive_other_pricelists": {
                "comment": "Archive other pricelists, stupid method, the code should be in setupCLass instead"
            }
        }
    },
    "ProductAttributesCommon": {
        "inherits": [
            "ProductCommon"
        ],
        "properties": {
            "size_attribute": {
                "type": "product.attribute",
                "comment": "A new attribute"
            },
            "size_attribute_s": {
                "type": "product.attribute.value"
            },
            "size_attribute_m": {
                "type": "product.attribute.value"
            },
            "size_attribute_l": {
                "type": "product.attribute.value"
            },
            "color_attribute": {
                "type": "product.attribute",
                "comment": "A new attribute"
            },
            "color_attribute_red": {
                "type": "product.attribute.value"
            },
            "color_attribute_blue": {
                "type": "product.attribute.value"
            },
            "color_attribute_green": {
                "type": "product.attribute.value"
            },
            "no_variant_attribute": {
                "type": "product.attribute",
                "comment": "A new attribute with no create"
            },
            "no_variant_attribute_extra": {
                "type": "product.attribute.value"
            },
            "no_variant_attribute_second": {
                "type": "product.attribute.value"
            },
            "dynamic_attribute": {
                "type": "product.attribute",
                "comment": "A new attribute with dynamic create, values dyn1 and dyn2"
            }
        }
    },
    "ProductVariantsCommon": {
        "inherits": [
            "ProductAttributesCommon"
        ],
        "properties": {
            "product_template_sofa": {
                "type": "product.template",
                "comment": "A new product template, with three cls.color_attribute values."
            },
            "cls.product_template_shirt": {
                "type": "product.template",
                "comment": "A new product template, with on cls.size_attribute value"
            }
        }
    },
    "TestProductCommon": {
        "inherits": [
            "ProductVariantsCommon"
        ],
        "properties": {
            "uom_dunit": {
                "type": "uom.uom",
                "comment": "Deci Unit, 10 x unit"
            },
            "product_1": {
                "type": "product.product",
                "value": "[PROD-1] Courage",
                "comment": "a new consumable product, no categ, uom_dunit"
            },
            "product_2": {
                "type": "product.product",
                "value": "Wood",
                "comment": "a new consumable product, no categ, no nothing"
            }
        },
        "prod_att_1": {
            "type": "product.attribute",
            "value": "cls.color_attribute"
        },
        "prod_attr1_v1": {
            "type": "product.attribute.value",
            "value": "cls.color_attribute_red"
        },
        "prod_attr1_v2": {
            "type": "product.attribute.value",
            "value": "cls.color_attribute_blue"
        },
        "prod_attr1_v3": {
            "type": "product.attribute.value",
            "value": "cls.color_attribute_green"
        },
        "product_7_template": {
            "type": "product.template",
            "value": "cls.product_template_sofa",
            "comment": "Pointer to cls.product_template_sofa"
        },
        "product_7_attr1_v1": {
            "type": "product.template.attribute.value"
        },
        "product_7_attr1_v2": {
            "type": "product.template.attribute.value"
        },
        "product_7_attr1_v3": {
            "type": "product.template.attribute.value"
        },
        "product_7_1": {
            "type": "product.product",
            "comment": "Variant of cls.product_7_attr1_v1"
        },
        "product_7_2": {
            "type": "product.product",
            "comment": "Variant of cls.product_7_attr1_v2"
        },
        "product_7_3": {
            "type": "product.product",
            "comment": "Variant of cls.product_7_attr1_v3"
        }
    },
    "common2.TestStockCommon": {
        "inherits": [
            "TestProductCommon"
        ],
        "properties": {
            "user_stock_user": {
                "type": "res.users",
                "value": "pauline",
                "comment": "New user with 'stock.group_stock_user' group"
            },
            "user_stock_manager": {
                "type": "res.users",
                "value": "julie",
                "comment": "New user with 'stock.group_stock_manager' group"
            },
            "warehouse_1": {
                "type": "stock.warehouse",
                "comment": "New warehouse with one step in and out",
                "value": "BWH"
            },
            "location_1": {
                "type": "stock.location",
                "comment": "Internal stock location of cls.warehouse_1",
                "value": "cls.warehouse_1.lot_stock_id.id"
            },
            "partner_1": {
                "type": "res.partner",
                "comment": "new partner"
            },
            "product_3": {
                "type": "product.product",
                "comment": "New consu product, in dozens",
                "value": "Stone"
            },
            "existing_inventories": {
                "type": "stock.quant",
                "comment": "Stock quants with inventory qty"
            },
            "existing_quants": {
                "type": "stock.quant",
                "comment": "All existing quands in the universe"
            }
        },
        "methods": {
            "_create_move": {
                "comment": "Create a stock move as stock manager"
            }
        }
    }
}


def get_available_attributes(test_class):
    if test_class not in data:
        return {}
    inherits = list(data[test_class].get("inherits", []))
    properties = dict(**data[test_class].get("properties", {}))
    methods = dict(**data[test_class].get("methods", {}))
    while inherits:
        parent = data.get(inherits.pop())
        if not parent:
            continue
        if parent.get("inherits"):
            inherits.extend(parent["inherits"])
        for prop, value_dict in parent.get("properties", {}).items():
            properties.setdefault(prop, dict(**value_dict))
        for method, value_dict in parent.get("methods", {}).items():
            methods.setdefault(method, dict(**value_dict))

    return {
        "properties": properties,
        "methods": methods
    }



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"""
The hitchhiker's guide to common tests.
=======================================
Usage: {sys.argv[0]} <common_test_class_name>"
 
If the class name is not unique add the unit file name,
if still not unique, add module. e.g. common2.TestStockCommon
""")
        sys.exit(1)
    common_class = sys.argv[1]
    print(dumps(get_available_attributes(common_class), indent=2))

