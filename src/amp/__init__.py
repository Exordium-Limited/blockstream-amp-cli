import argparse


def main():
    parser = argparse.ArgumentParser(description="Blockstream AMP CLI tool.")
    parser.add_argument("--profile", help="Profile name to load from ~/.amp/profiles")

    subparsers = parser.add_subparsers(help="sub-command help", dest="command")

    """ Assets Management """
    parser_assets = subparsers.add_parser("assets", help="Assets management.")
    subparser_assets = parser_assets.add_subparsers(
        help="sub-command help", dest="subcommand"
    )

    parser_assets_list = subparser_assets.add_parser(
        "list", help="List the issued assets.", aliases=["ls"]
    )

    parser_assets_edit = subparser_assets.add_parser(
        "edit",
        help="Edit an asset. Only the issuser authorization endpoint can be updated.",
    )
    parser_assets_edit.add_argument("asset_uuid", help="Asset UUID")
    parser_assets_edit.add_argument(
        "-endpoint", "--endpoint", help="Issuer Authorization Endpoint", required=True
    )

    parser_assets_remove = subparser_assets.add_parser(
        "remove",
        help="Remove an asset from AMP (non-reversible operation!).",
        aliases=["rm"],
    )
    parser_assets_remove.add_argument("asset_uuid", help="Asset UUID")

    parser_assets_issue = subparser_assets.add_parser(
        "issue", help="Issue an asset (non-reversible operation!)."
    )
    parser_assets_issue.add_argument("-name", "--name", help="Asset Name")

    parser_assets_reissue = subparser_assets.add_parser(
        "reissue", help="Reissue an asset (non-reversible operation!)."
    )
    parser_assets_reissue.add_argument("asset_uuid", help="Asset UUID")
    parser_assets_reissue.add_argument(
        "-amount", "--amount", help="Amount of asset to reissue", required=True
    )

    parser_assets_authorize = subparser_assets.add_parser(
        "authorize", help="Enforce the asset to be used only by authorized categories."
    )
    parser_assets_authorize.add_argument("asset_uuid", help="Asset UUID")

    parser_assets_register = subparser_assets.add_parser(
        "register", help="Register on the Blockstream Liquid Assets Registry."
    )
    parser_assets_register.add_argument("asset_uuid", help="Asset UUID")

    parser_assets_details = subparser_assets.add_parser(
        "details", help="Retrieves the details of a given asset."
    )
    parser_assets_details.add_argument("asset_uuid", help="Asset UUID")

    parser_assets_owners = subparser_assets.add_parser(
        "owners", help="Dumps the entire list of current owners of a given asset."
    )
    parser_assets_owners.add_argument("asset_uuid", help="Asset UUID")

    parser_assets_lock = subparser_assets.add_parser(
        "lock", help="Enforce the asset to not be transferable."
    )
    parser_assets_lock.add_argument("asset_uuid", help="Asset UUID")

    parser_assets_unlock = subparser_assets.add_parser(
        "unlock", help="Free the asset to be transferable."
    )
    parser_assets_unlock.add_argument("asset_uuid", help="Asset UUID")

    """ Treasury Addresses Management """
    parser_assets_treasury = subparser_assets.add_parser(
        "treasury", help="Manage the treasury addresses of a given asset."
    )
    subparser_assets_treasury = parser_assets_treasury.add_subparsers(
        help="sub-command help", dest="function"
    )

    parser_assets_treasury_list = subparser_assets_treasury.add_parser(
        "list", help="List the treasury addresses of a given asset.", aliases=["ls"]
    )
    parser_assets_treasury_list.add_argument("asset_uuid", help="Asset UUID")

    parser_assets_treasury_add = subparser_assets_treasury.add_parser(
        "add", help="Add an address to the treasury addresses of a given asset."
    )
    parser_assets_treasury_add.add_argument("asset_uuid", help="Asset UUID")
    parser_assets_treasury_add.add_argument(
        "-address",
        "--address",
        help="Liquid Address to add to the treasury",
        required=True,
    )

    """ UTXOs management """
    parser_assets_utxos = subparser_assets.add_parser(
        "utxos", help="Manage the UTXOs of a given asset."
    )
    subparser_assets_utxos = parser_assets_utxos.add_subparsers(
        help="sub-command help", dest="function"
    )

    parser_assets_utxos_list = subparser_assets_utxos.add_parser(
        "list", help="List the UTXOs of a given asset.", aliases=["ls"]
    )
    parser_assets_utxos_list.add_argument("asset_uuid", help="Asset UUID")

    parser_assets_utxos_block = subparser_assets_utxos.add_parser(
        "block", help="Block a specific UTXO of a given asset."
    )
    parser_assets_utxos_block.add_argument("asset_uuid", help="Asset UUID")
    parser_assets_utxos_block.add_argument(
        "-txid", "--txid", help="Transaction id of the UTXO", required=True
    )
    parser_assets_utxos_block.add_argument(
        "-vout", "--vout", help="Vout of the UTXO", required=True
    )

    """ Assignments """
    parser_assignments = subparsers.add_parser(
        "assignments", help="Assignments management."
    )
    subparser_assignments = parser_assignments.add_subparsers(
        help="sub-command help", dest="subcommand"
    )

    parser_assignments_list = subparser_assignments.add_parser(
        "list", help="List the assigments.", aliases=["ls"]
    )
    parser_assignments_list.add_argument("asset_uuid", help="Asset UUID")
    group_parser_assignments_list = (
        parser_assignments_list.add_mutually_exclusive_group()
    )
    group_parser_assignments_list.add_argument(
        "-all", "--all", help="All assignments", action="store_true"
    )
    group_parser_assignments_list.add_argument(
        "-distributed",
        "--distributed",
        help="Non distributed assignments",
        action="store_true",
    )
    group_parser_assignments_list.add_argument(
        "-nondistributed",
        "--non_distributed",
        help="Non distributed assignments",
        action="store_true",
    )

    parser_assignments_details = subparser_assignments.add_parser(
        "details", help="Details of a given assigment."
    )
    parser_assignments_details.add_argument("asset_uuid", help="Asset UUID")
    parser_assignments_details.add_argument(
        "-id", "--assignment_id", help="Assignment ID", required=True
    )

    parser_assignments_remove = subparser_assignments.add_parser(
        "remove",
        help="Remove a given assigment (non-reversible operation!).",
        aliases=["rm"],
    )
    parser_assignments_remove.add_argument("asset_uuid", help="Asset UUID")
    parser_assignments_remove.add_argument(
        "-id", "--assignment_id", help="Assignment ID", required=True
    )

    parser_assignments_create = subparser_assignments.add_parser(
        "create", help="Create an assigment."
    )
    parser_assignments_create.add_argument("asset_uuid", help="Asset UUID")
    parser_assignments_create.add_argument(
        "-uid", "--user_id", help="User ID", required=True
    )
    parser_assignments_create.add_argument(
        "-a", "--amount", help="Assignment amount", required=True
    )

    """ Catogories """
    parser_categories = subparsers.add_parser(
        "categories", help="Categories management."
    )
    subparser_categories = parser_categories.add_subparsers(
        help="sub-command help", dest="subcommand"
    )

    parser_categories_list = subparser_categories.add_parser(
        "list", help="List the categories.", aliases=["ls"]
    )

    parser_categories_create = subparser_categories.add_parser(
        "create", help="Create a category."
    )
    parser_categories_create.add_argument("category_name", help="Category name")
    parser_categories_create.add_argument(
        "-desc", "--description", help="Category description", required=True
    )

    parser_categories_associate = subparser_categories.add_parser(
        "associate", help="Associate an asset to a category."
    )
    parser_categories_associate.add_argument("category_id", help="Cateogry ID")
    parser_categories_associate.add_argument("asset_uuid", help="Asset UUID")

    parser_categories_register = subparser_categories.add_parser(
        "register", help="Register a user in a category."
    )
    parser_categories_register.add_argument("category_id", help="Cateogry ID")
    parser_categories_register.add_argument("user_id", help="User ID")

    parser_categories_unregister = subparser_categories.add_parser(
        "unregister", help="Unregister a user from a category."
    )
    parser_categories_unregister.add_argument("category_id", help="Cateogry ID")
    parser_categories_unregister.add_argument("user_id", help="User ID")

    """ Distributions """
    parser_distributions = subparsers.add_parser(
        "distributions", help="Distributions management."
    )
    subparser_distributions = parser_distributions.add_subparsers(
        help="sub-command help", dest="subcommand"
    )

    parser_distributions_list = subparser_distributions.add_parser(
        "list", help="List the distributions.", aliases=["ls"]
    )

    parser_distributions_details = subparser_distributions.add_parser(
        "details", help="Details of a given distribution."
    )
    parser_distributions_details.add_argument("asset_uuid", help="Asset UUID")
    parser_distributions_details.add_argument(
        "-id", "--distribution_id", help="Distribution ID", required=True
    )

    parser_distributions_prepare = subparser_distributions.add_parser(
        "prepare", help="Prepare a distribution of the current assignments."
    )
    parser_distributions_prepare.add_argument("asset_uuid", help="Asset UUID")

    parser_distributions_cancel = subparser_distributions.add_parser(
        "details", help="Cancel a given distribution."
    )
    parser_distributions_cancel.add_argument("asset_uuid", help="Asset UUID")
    parser_distributions_cancel.add_argument(
        "-id", "--distribution_id", help="Distribution ID", required=True
    )

    """ Registered Users """
    parser_users = subparsers.add_parser("users", help="Users management.")
    subparser_users = parser_users.add_subparsers(
        help="sub-command help", dest="subcommand"
    )

    parser_users_list = subparser_users.add_parser(
        "list", help="List the users.", aliases=["ls"]
    )

    parser_users_create = subparser_users.add_parser("create", help="Create a user.")
    parser_users_create.add_argument(
        "-gaid", "--user_gaid", help="User GAID", required=True
    )
    parser_users_create.add_argument(
        "-fullname", "--user_fullname", help="User Full Name", required=True
    )
    parser_users_create.add_argument(
        "-company",
        "--is_company",
        help="Is a company",
        required=False,
        action="store_true",
    )

    parser_users_edit = subparser_users.add_parser("edit", help="Edit a user.")
    parser_users_edit.add_argument("user_id", help="Asset UUID")
    parser_users_edit.add_argument(
        "-fullname", "--user_fullname", help="User Full Name", required=True
    )

    parser_users_remove = subparser_users.add_parser(
        "remove",
        help="Remove a given user (non-reversible operation!).",
        aliases=["rm"],
    )
    parser_users_remove.add_argument("user_id", help="Asset UUID")

    """ GAIDs """
    parser_gaids = subparsers.add_parser("gaids", help="GAID management.")
    subparser_gaids = parser_gaids.add_subparsers(
        help="sub-command help", dest="subcommand"
    )

    parser_gaids_validate = subparser_gaids.add_parser(
        "validate", help="Verify the validity of a GAID."
    )
    parser_gaids_validate.add_argument("gaid", help="The GAID to validate")

    """ Managers """
    parser_managers = subparsers.add_parser("managers", help="Managers management.")
    subparser_managers = parser_managers.add_subparsers(
        help="sub-command help", dest="subcommand"
    )

    parser_managers_create = subparser_managers.add_parser(
        "create", help="Create a manager."
    )
    parser_managers_create.add_argument("username", help="Username")
    parser_managers_create.add_argument("password", help="Password")

    parser_managers_associate = subparser_managers.add_parser(
        "associate", help="Associate an asset to a manager."
    )
    parser_managers_associate.add_argument("manager_id", help="Manager ID")
    parser_managers_associate.add_argument("asset_uuid", help="Asset UUID")

    """ Account """
    parser_account = subparsers.add_parser("account", help="Account management.")
    subparser_account = parser_account.add_subparsers(
        help="sub-command help", dest="subcommand"
    )

    parser_account_passwd = subparser_account.add_parser(
        "change_password",
        help="Change the password of your account.",
        aliases=["passwd"],
    )
    parser_account_passwd.add_argument(
        "-old", "--old_password", help="Current API password", required=True
    )
    parser_account_passwd.add_argument(
        "-new", "--new_password", help="New API password", required=True
    )

    """ Parsing of the command """
    args = parser.parse_args()

    import importlib

    module = importlib.import_module(f"amp.commands.{args.command}")
    action = getattr(
        module,
        f"{args.subcommand}_{args.function}" if "function" in args else args.subcommand,
    )

    kwargs = vars(args)

    # If a specific profile is requested, use it.
    if args.profile:
        import amp.api as api

        api.setProfile(args.profile)

    action(**kwargs)
