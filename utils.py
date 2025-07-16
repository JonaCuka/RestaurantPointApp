from enums import UserFeauters, UserRole
from admin_view import RestaurantManagerContentPanel, MenuManagerContentPanel, MenuItemManagerContentPanel, TableManagerContentPanel

class AuthorizationServices:

    def get_user_feature_by_user_role(self, user_role):
       # if user_role is None:
           # return []  
        #user_role = user.user_role  
        match (user_role):
            case UserRole.MANAGER:
                return [UserFeauters.RESTAURANT_MANAGER,UserFeauters.MENU_MANAGER, UserFeauters.MENU_ITEM_MANAGER,  UserFeauters.TABLE_MANAGER, UserFeauters.SIGN_OUT]
            case UserRole.WAITER:
                return [UserFeauters.TABLE_ORDERS, UserFeauters.ORDER_STATUS, UserFeauters.SIGN_OUT]
            case UserRole.COOKER:
                return [UserFeauters.TABLE_ORDERS, UserFeauters.ORDER_STATUS, UserFeauters.SIGN_OUT]
            case _:
                return RuntimeError("Invalid User Role")


class UserFeaturesContentPanelResolver: 
    user_feature_content_panel_dict = None

    @staticmethod
    def get_user_feature_panel(user_feature):

        return UserFeaturesContentPanelResolver.get_user_feature_content_panel_dict().get(user_feature).create_content_panel()

    def get_user_feature_content_panel_dict():
        if UserFeaturesContentPanelResolver.user_feature_content_panel_dict is None:
            user_feature_content_panel_dict = {
                UserFeauters.RESTAURANT_MANAGER : RestaurantManagerContentPanel(),
                UserFeauters.MENU_MANAGER : MenuManagerContentPanel(),
                UserFeauters.MENU_ITEM_MANAGER : MenuItemManagerContentPanel(),
                UserFeauters.TABLE_MANAGER : TableManagerContentPanel()
                
           }
        return user_feature_content_panel_dict


