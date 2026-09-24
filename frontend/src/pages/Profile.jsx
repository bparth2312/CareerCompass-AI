import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  FaArrowLeft,
  FaEnvelope,
  FaKey,
  FaSave,
  FaShieldAlt,
  FaUser
} from "react-icons/fa";

import ThemeToggle from "../components/ThemeToggle/ThemeToggle";

import {
  changeUserPassword,
  getUserProfile,
  updateUserProfile
} from "../services/userService";


const getErrorMessage = (
  error,
  fallbackMessage
) => {
  const detail = error.response?.data?.detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === "string") {
          return item;
        }

        if (item?.msg) {
          return item.msg;
        }

        if (item?.message) {
          return item.message;
        }

        return "Validation error";
      })
      .join(", ");
  }

  if (
    detail &&
    typeof detail === "object"
  ) {
    return (
      detail.message ||
      "An unexpected error occurred."
    );
  }

  if (error.message === "Network Error") {
    return (
      "Unable to connect to the backend. " +
      "Make sure FastAPI is running."
    );
  }

  return fallbackMessage;
};


function Profile() {
  const navigate = useNavigate();

  const [profile, setProfile] = useState({
    full_name: "",
    email: ""
  });

  const [passwordForm, setPasswordForm] =
    useState({
      current_password: "",
      new_password: "",
      confirm_password: ""
    });

  const [isLoading, setIsLoading] =
    useState(true);

  const [
    isSavingProfile,
    setIsSavingProfile
  ] = useState(false);

  const [
    isChangingPassword,
    setIsChangingPassword
  ] = useState(false);

  const [
    errorMessage,
    setErrorMessage
  ] = useState("");

  const [
    successMessage,
    setSuccessMessage
  ] = useState("");

  useEffect(() => {
    const loadProfile = async () => {
      setIsLoading(true);
      setErrorMessage("");
      setSuccessMessage("");

      try {
        const data =
          await getUserProfile();

        setProfile({
          full_name:
            data.full_name || "",
          email:
            data.email || ""
        });
      } catch (error) {
        console.error(
          "Profile loading error:",
          error
        );

        if (
          error.response?.status === 401
        ) {
          localStorage.removeItem(
            "token"
          );

          navigate("/login", {
            replace: true
          });

          return;
        }

        setErrorMessage(
          getErrorMessage(
            error,
            "Unable to load your profile."
          )
        );
      } finally {
        setIsLoading(false);
      }
    };

    loadProfile();
  }, [navigate]);

  const handleProfileChange = (
    event
  ) => {
    const { name, value } =
      event.target;

    setProfile((currentProfile) => ({
      ...currentProfile,
      [name]: value
    }));
  };

  const handlePasswordChange = (
    event
  ) => {
    const { name, value } =
      event.target;

    setPasswordForm(
      (currentForm) => ({
        ...currentForm,
        [name]: value
      })
    );
  };

  const handleProfileSubmit =
    async (event) => {
      event.preventDefault();

      setErrorMessage("");
      setSuccessMessage("");

      const cleanedFullName =
        profile.full_name.trim();

      if (
        cleanedFullName.length < 2
      ) {
        setErrorMessage(
          "Full name must contain at least 2 characters."
        );

        return;
      }

      setIsSavingProfile(true);

      try {
        const updatedProfile =
          await updateUserProfile({
            full_name:
              cleanedFullName
          });

        setProfile({
          full_name:
            updatedProfile.full_name ||
            "",
          email:
            updatedProfile.email || ""
        });

        setSuccessMessage(
          "Profile updated successfully."
        );
      } catch (error) {
        console.error(
          "Profile update error:",
          error
        );

        if (
          error.response?.status ===
          401
        ) {
          localStorage.removeItem(
            "token"
          );

          navigate("/login", {
            replace: true
          });

          return;
        }

        setErrorMessage(
          getErrorMessage(
            error,
            "Unable to update your profile."
          )
        );
      } finally {
        setIsSavingProfile(false);
      }
    };

  const handlePasswordSubmit =
    async (event) => {
      event.preventDefault();

      setErrorMessage("");
      setSuccessMessage("");

      const {
        current_password,
        new_password,
        confirm_password
      } = passwordForm;

      if (
        !current_password ||
        !new_password ||
        !confirm_password
      ) {
        setErrorMessage(
          "Please complete all password fields."
        );

        return;
      }

      if (
        new_password.length < 6
      ) {
        setErrorMessage(
          "New password must contain at least 6 characters."
        );

        return;
      }

      if (
        new_password !==
        confirm_password
      ) {
        setErrorMessage(
          "New password and confirm password do not match."
        );

        return;
      }

      if (
        current_password ===
        new_password
      ) {
        setErrorMessage(
          "New password must be different from the current password."
        );

        return;
      }

      setIsChangingPassword(true);

      try {
        const response =
          await changeUserPassword({
            current_password,
            new_password,
            confirm_password
          });

        setSuccessMessage(
          response.message ||
            "Password changed successfully."
        );

        setPasswordForm({
          current_password: "",
          new_password: "",
          confirm_password: ""
        });
      } catch (error) {
        console.error(
          "Password change error:",
          error
        );

        if (
          error.response?.status ===
          401
        ) {
          localStorage.removeItem(
            "token"
          );

          navigate("/login", {
            replace: true
          });

          return;
        }

        setErrorMessage(
          getErrorMessage(
            error,
            "Unable to change your password."
          )
        );
      } finally {
        setIsChangingPassword(false);
      }
    };

  if (isLoading) {
    return (
      <main className="app-page">
        <div className="page-container max-w-[1400px]">
          <div className="state-container">
            <div className="spinner" />

            <p className="state-title">
              Loading your profile
            </p>

            <p className="state-message">
              Please wait while we retrieve your account
              information.
            </p>
          </div>
        </div>
      </main>
    );
  }

  return (
    <main className="app-page">
      <div className="page-container max-w-[1400px]">

        <header className="
          flex flex-col gap-5
          border-b border-[var(--border)]
          pb-6
          md:flex-row
          md:items-center
          md:justify-between
        ">
          <div>
            <p className="
              text-sm font-semibold
              text-[var(--primary)]
            ">
              CareerCompass
            </p>

            <h1 className="page-title mt-2">
              My Profile
            </h1>

            <p className="page-subtitle">
              Manage your personal information and keep
              your account secure.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <ThemeToggle />

            <button
              type="button"
              onClick={() => navigate("/dashboard")}
              className="btn-outline"
            >
              <FaArrowLeft />
              Back to Dashboard
            </button>
          </div>
        </header>


        {errorMessage && (
          <div className="
            mt-6 rounded-2xl
            border border-red-300
            bg-red-50 p-4
            text-red-800

            dark:border-red-900/70
            dark:bg-red-950/30
            dark:text-red-300
          ">
            {errorMessage}
          </div>
        )}

        {successMessage && (
          <div className="
            mt-6 rounded-2xl
            border border-green-300
            bg-green-50 p-4
            text-green-800

            dark:border-green-900/70
            dark:bg-green-950/30
            dark:text-green-300
          ">
            {successMessage}
          </div>
        )}


        <section className="
          mt-8 grid gap-7
          lg:grid-cols-2
        ">
          <article className="app-card app-card-padding">
            <div className="flex items-center gap-4">
              <div className="
                flex h-12 w-12
                items-center justify-center
                rounded-2xl
                bg-[var(--primary-soft)]
                text-xl
                text-[var(--primary)]
              ">
                <FaUser />
              </div>

              <div>
                <h2 className="section-title">
                  Personal Information
                </h2>

                <p className="section-description">
                  Update the name shown on your account.
                </p>
              </div>
            </div>

            <form
              onSubmit={handleProfileSubmit}
              className="mt-7 space-y-5"
            >
              <div className="form-group">
                <label
                  htmlFor="full_name"
                  className="form-label"
                >
                  Full Name
                </label>

                <div className="relative">
                  <FaUser className="
                    pointer-events-none
                    absolute left-4 top-1/2
                    z-10 -translate-y-1/2
                    text-[var(--text-muted)]
                  " />

                  <input
                    id="full_name"
                    name="full_name"
                    type="text"
                    value={profile.full_name}
                    onChange={handleProfileChange}
                    placeholder="Enter your full name"
                    autoComplete="name"
                    required
                    className="form-input"
                    style={{
                      paddingLeft: "2.9rem"
                    }}
                  />
                </div>
              </div>


              <div className="form-group">
                <label
                  htmlFor="email"
                  className="form-label"
                >
                  Email Address
                </label>

                <div className="relative">
                  <FaEnvelope className="
                    pointer-events-none
                    absolute left-4 top-1/2
                    z-10 -translate-y-1/2
                    text-[var(--text-muted)]
                  " />

                  <input
                    id="email"
                    name="email"
                    type="email"
                    value={profile.email}
                    disabled
                    className="
                      form-input
                      cursor-not-allowed
                      bg-[var(--surface-soft)]
                      text-[var(--text-muted)]
                    "
                    style={{
                      paddingLeft: "2.9rem"
                    }}
                  />
                </div>

                <p className="form-help">
                  Email cannot currently be changed.
                </p>
              </div>


              <button
                type="submit"
                disabled={isSavingProfile}
                className="
                  btn-primary w-full
                  disabled:cursor-not-allowed
                  disabled:opacity-50
                "
              >
                <FaSave />

                {isSavingProfile
                  ? "Saving..."
                  : "Save Profile"}
              </button>
            </form>
          </article>


          <article className="app-card app-card-padding">
            <div className="flex items-center gap-4">
              <div className="
                flex h-12 w-12
                items-center justify-center
                rounded-2xl
                bg-[var(--accent-soft)]
                text-xl
                text-[var(--warning)]
              ">
                <FaKey />
              </div>

              <div>
                <h2 className="section-title">
                  Change Password
                </h2>

                <p className="section-description">
                  Choose a strong password that you do not
                  use on other websites.
                </p>
              </div>
            </div>

            <form
              onSubmit={handlePasswordSubmit}
              className="mt-7 space-y-5"
            >
              <PasswordInput
                id="current_password"
                label="Current Password"
                name="current_password"
                value={passwordForm.current_password}
                onChange={handlePasswordChange}
                placeholder="Enter current password"
                autoComplete="current-password"
              />

              <PasswordInput
                id="new_password"
                label="New Password"
                name="new_password"
                value={passwordForm.new_password}
                onChange={handlePasswordChange}
                placeholder="Enter new password"
                autoComplete="new-password"
              />

              <PasswordInput
                id="confirm_password"
                label="Confirm New Password"
                name="confirm_password"
                value={passwordForm.confirm_password}
                onChange={handlePasswordChange}
                placeholder="Confirm new password"
                autoComplete="new-password"
              />

              <button
                type="submit"
                disabled={isChangingPassword}
                className="
                  btn-secondary w-full
                  disabled:cursor-not-allowed
                  disabled:opacity-50
                "
              >
                <FaKey />

                {isChangingPassword
                  ? "Changing Password..."
                  : "Change Password"}
              </button>
            </form>
          </article>
        </section>


        <aside className="
          mt-7
          rounded-2xl
          border border-[var(--border)]
          bg-[var(--surface-soft)]
          p-5
        ">
          <div className="flex items-start gap-3">
            <FaShieldAlt className="
              mt-1 shrink-0
              text-[var(--primary)]
            " />

            <div>
              <h2 className="
                font-semibold
                text-[var(--text-primary)]
              ">
                Account security
              </h2>

              <p className="
                mt-2 text-sm leading-6
                text-[var(--text-secondary)]
              ">
                Never share your password. Use a unique
                password with letters, numbers and symbols.
              </p>
            </div>
          </div>
        </aside>
      </div>
    </main>
  );
}


function PasswordInput({
  id,
  label,
  name,
  value,
  onChange,
  placeholder,
  autoComplete
}) {
  return (
    <div className="form-group">
      <label
        htmlFor={id}
        className="form-label"
      >
        {label}
      </label>

      <div className="relative">
        <FaKey className="
          pointer-events-none
          absolute left-4 top-1/2
          z-10 -translate-y-1/2
          text-[var(--text-muted)]
        " />

        <input
          id={id}
          name={name}
          type="password"
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          autoComplete={autoComplete}
          required
          className="form-input"
          style={{
            paddingLeft: "2.9rem"
          }}
        />
      </div>
    </div>
  );
}

export default Profile;