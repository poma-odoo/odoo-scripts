#!/usr/bin/env python3
from json import dumps
import sys

data = {
    "BaseCommon": {
        "inherits": [],
        "attributes": {
            "env": {
                "type": "Environment",
                "comment": "With disabled mail tracking",
            },
            "partner": {
                "type": "recordset",
                "relation": "res.partner",
                "comment": "a new partner",
            },
            "currency": {
                "type": "recordset",
                "relation": "res.currency",
                "comment": "company_id.currency_id",
            },
        },
    },
    "UomCommon": {
        "inherits": [],
        "attributes": {
            "uom_gram": {"type": "recordset", "relation": "uom.uom"},
            "uom_kgm": {"type": "recordset", "relation": "uom.uom"},
            "uom_ton": {"type": "recordset", "relation": "uom.uom"},
            "uom_unit": {"type": "recordset", "relation": "uom.uom"},
            "uom_dozen": {"type": "recordset", "relation": "uom.uom"},
            "group_uom": {
                "type": "recordset",
                "relation": "res.groups",
                "comment": "Security group of uom access",
            },
            "_enable_uom": {
                "type": "method",
                "comment": "Enable uom group for current env's user",
            },
            "_disable_uom": {
                "type": "method",
                "comment": "Disable uom group for current env's user",
            },
        },
    },
    "ProductCommon": {
        "inherits": ["BaseCommon", "UomCommon"],
        "does": "Set env's company currency to usd, disable all pricelists.",
        "attributes": {
            "currency": {
                "type": "recordset",
                "relation": "res.currency",
                "value": "USD",
                "comment": "overrides BaseCommon.currency, also sets it as company currency",
            },
            "product_category": {
                "type": "recordset",
                "relation": "product.category",
                "comment": "a new category",
            },
            "product": {
                "type": "recordset",
                "relation": "product.product",
                "comment": "a new consumable product, in cls.product_category",
            },
            "service_product": {
                "type": "recordset",
                "relation": "product.product",
                "comment": "a new service product, in cls.product_category",
            },
            "consumable_product": {
                "type": "recordset",
                "relation": "product.product",
                "comment": "pointer to cls.product",
            },
            "pricelist": {
                "type": "recordset",
                "relation": "product.pricelist",
                "comment": "a new pricelist",
            },
            "_archive_other_pricelists": {
                "type": "method",
                "comment": "Archive other pricelists, stupid method, the code should be in setupCLass instead",
            },
        },
    },
    "ProductAttributesCommon": {
        "inherits": ["ProductCommon"],
        "attributes": {
            "size_attribute": {
                "type": "recordset",
                "relation": "product.attribute",
                "comment": "A new attribute",
            },
            "size_attribute_s": {
                "type": "recordset",
                "relation": "product.attribute.value",
            },
            "size_attribute_m": {
                "type": "recordset",
                "relation": "product.attribute.value",
            },
            "size_attribute_l": {
                "type": "recordset",
                "relation": "product.attribute.value",
            },
            "color_attribute": {
                "type": "recordset",
                "relation": "product.attribute",
                "comment": "A new attribute",
            },
            "color_attribute_red": {
                "type": "recordset",
                "relation": "product.attribute.value",
            },
            "color_attribute_blue": {
                "type": "recordset",
                "relation": "product.attribute.value",
            },
            "color_attribute_green": {
                "type": "recordset",
                "relation": "product.attribute.value",
            },
            "no_variant_attribute": {
                "type": "recordset",
                "relation": "product.attribute",
                "comment": "A new attribute with no create",
            },
            "no_variant_attribute_extra": {
                "type": "recordset",
                "relation": "product.attribute.value",
            },
            "no_variant_attribute_second": {
                "type": "recordset",
                "relation": "product.attribute.value",
            },
            "dynamic_attribute": {
                "type": "recordset",
                "relation": "product.attribute",
                "comment": "A new attribute with dynamic create, values dyn1 and dyn2",
            },
        },
    },
    "ProductVariantsCommon": {
        "inherits": ["ProductAttributesCommon"],
        "attributes": {
            "product_template_sofa": {
                "type": "recordset",
                "relation": "product.template",
                "comment": "A new product template, with three cls.color_attribute values.",
            },
            "cls.product_template_shirt": {
                "type": "recordset",
                "relation": "product.template",
                "comment": "A new product template, with on cls.size_attribute value",
            },
        },
    },
    "TestProductCommon": {
        "inherits": ["ProductVariantsCommon"],
        "attributes": {
            "uom_dunit": {
                "type": "recordset",
                "relation": "uom.uom",
                "comment": "Deci Unit, 10 x unit",
            },
            "product_1": {
                "type": "recordset",
                "relation": "product.product",
                "value": "[PROD-1] Courage",
                "comment": "a new consumable product, no categ, uom_dunit",
            },
            "product_2": {
                "type": "recordset",
                "relation": "product.product",
                "value": "Wood",
                "comment": "a new consumable product, no categ, no nothing",
            },
        },
        "prod_att_1": {
            "type": "recordset",
            "relation": "product.attribute",
            "value": "cls.color_attribute",
        },
        "prod_attr1_v1": {
            "type": "recordset",
            "relation": "product.attribute.value",
            "value": "cls.color_attribute_red",
        },
        "prod_attr1_v2": {
            "type": "recordset",
            "relation": "product.attribute.value",
            "value": "cls.color_attribute_blue",
        },
        "prod_attr1_v3": {
            "type": "recordset",
            "relation": "product.attribute.value",
            "value": "cls.color_attribute_green",
        },
        "product_7_template": {
            "type": "recordset",
            "relation": "product.template",
            "value": "cls.product_template_sofa",
            "comment": "Pointer to cls.product_template_sofa",
        },
        "product_7_attr1_v1": {
            "type": "recordset",
            "relation": "product.template.attribute.value",
        },
        "product_7_attr1_v2": {
            "type": "recordset",
            "relation": "product.template.attribute.value",
        },
        "product_7_attr1_v3": {
            "type": "recordset",
            "relation": "product.template.attribute.value",
        },
        "product_7_1": {
            "type": "recordset",
            "relation": "product.product",
            "comment": "Variant of cls.product_7_attr1_v1",
        },
        "product_7_2": {
            "type": "recordset",
            "relation": "product.product",
            "comment": "Variant of cls.product_7_attr1_v2",
        },
        "product_7_3": {
            "type": "recordset",
            "relation": "product.product",
            "comment": "Variant of cls.product_7_attr1_v3",
        },
    },
    "common2.TestStockCommon": {
        "inherits": ["TestProductCommon"],
        "attributes": {
            "user_stock_user": {
                "type": "recordset",
                "relation": "res.users",
                "value": "pauline",
                "comment": "New user with 'stock.group_stock_user' group",
            },
            "user_stock_manager": {
                "type": "recordset",
                "relation": "res.users",
                "value": "julie",
                "comment": "New user with 'stock.group_stock_manager' group",
            },
            "warehouse_1": {
                "type": "recordset",
                "relation": "stock.warehouse",
                "comment": "New warehouse with one step in and out",
                "value": "BWH",
            },
            "location_1": {
                "type": "recordset",
                "relation": "stock.location",
                "comment": "Internal stock location of cls.warehouse_1",
                "value": "cls.warehouse_1.lot_stock_id.id",
            },
            "partner_1": {
                "type": "recordset",
                "relation": "res.partner",
                "comment": "new partner",
            },
            "product_3": {
                "type": "recordset",
                "relation": "product.product",
                "comment": "New consu product, in dozens",
                "value": "Stone",
            },
            "existing_inventories": {
                "type": "recordset",
                "relation": "stock.quant",
                "comment": "Stock quants with inventory qty",
            },
            "existing_quants": {
                "type": "recordset",
                "relation": "stock.quant",
                "comment": "All existing quands in the universe",
            },
            "_create_move": {
                "type": "method",
                "comment": "Create a stock move as stock manager",
            },
        },
    },
}


def get_available_attributes(test_class):
    if test_class not in data:
        return {}
    inherits = list(data[test_class].get("inherits", []))
    attributes = dict(**data[test_class].get("attributes", {}))
    while inherits:
        parent = data.get(inherits.pop())
        if not parent:
            continue
        if parent.get("inherits"):
            inherits.extend(parent["inherits"])
        for attrib, value_dict in parent.get("attributes", {}).items():
            attributes.setdefault(attrib, dict(**value_dict))

    return attributes


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            f"""
The hitchhiker's guide to common tests.
=======================================
Usage: {sys.argv[0]} <common_test_class_name>"
 
If the class name is not unique add the unit file name,
if still not unique, add module. e.g. common2.TestStockCommon
"""
        )
        sys.exit(1)
    query = sys.argv[1]
    common_classes = []
    if query in data:
        common_classes.append(query)
    else:
        print(f"Unknown common test class {query}, trying to find it heuristically...")
        for cls in data:
            if query in cls:
                print(f"Found common test class {cls}")
                common_classes.append(cls)

    if len(common_classes) == 0:
        print(f"Could not find common test class {sys.argv[1]}")
        sys.exit(1)
    for common_class in common_classes:
        if len(common_classes) > 1:
            print(f"======= {common_class} ========")
        print(dumps(get_available_attributes(common_class), indent=2))
