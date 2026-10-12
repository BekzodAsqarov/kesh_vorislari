def erp_context(request):
    user = getattr(request, "user", None)
    nav_items = []
    if user and user.is_authenticated:
        nav_items = [
            {"url_name": "dashboard:index", "namespace": "dashboard", "label": "Dashboard"},
        ]
        if user.is_admin or user.is_teacher:
            nav_items.extend(
                [
                    {"url_name": "children:list", "namespace": "children", "label": "Children"},
                    {"url_name": "groups:list", "namespace": "groups", "label": "Groups"},
                    {"url_name": "attendance:list", "namespace": "attendance", "label": "Attendance"},
                ]
            )
        else:
            nav_items.append({"url_name": "children:list", "namespace": "children", "label": "My children"})
        nav_items.extend(
            [
                {"url_name": "meals:list", "namespace": "meals", "label": "Meals"},
                {"url_name": "activities:list", "namespace": "activities", "label": "Activities"},
                {"url_name": "reports:list", "namespace": "reports", "label": "Daily reports"},
            ]
        )
        if user.is_admin:
            nav_items.append({"url_name": "accounts:users", "namespace": "accounts", "label": "Users"})
    return {
        "erp_name": "Kesh Vorislari ERP",
        "nav_items": nav_items,
    }
