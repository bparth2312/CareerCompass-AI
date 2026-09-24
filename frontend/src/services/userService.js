import api from "./api";

export const getUserProfile = async () => {
  const response = await api.get("/profile");
  return response.data;
};

export const updateUserProfile = async (profileData) => {
  const response = await api.put(
    "/profile",
    profileData
  );

  return response.data;
};

export const changeUserPassword = async (passwordData) => {
  const response = await api.put(
    "/profile/change-password",
    {
      current_password:
        passwordData.current_password,

      new_password:
        passwordData.new_password,

      confirm_password:
        passwordData.confirm_password
    }
  );

  return response.data;
};