<template>
    <div class="user-profile">

        <span class="user-name">{{ user.name }}</span>
        <button class="auth-button" @click="handleAuth">
            {{ isLoggedIn ? "Log Out" : "Log In" }}
            <img :src="isLoggedIn ? logoutSvg : loginSvg" :alt="isLoggedIn ? 'Log Out' : 'Log In'" class="auth-icon" />

        </button>
    </div>
</template>

<script>
import loginSvg from "@/assets/login.svg"
import logoutSvg from "@/assets/logout.svg"
export default {
    props: {
        user: {
            type: Object,
            required: true,
            default: () => ({ name: "Guest" }),
        },
    },
    computed: {
        isLoggedIn() {
            return !!this.user && !!this.user.isLoggedIn;
        },
    },
    methods: {
        handleAuth() {
            this.$emit("auth");
        },
    },
    data() {
        return {
            loginSvg,
            logoutSvg,
        };
    },
};
</script>

<style scoped>
.user-profile {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-color: var(--background-color);
    border-radius: 8px;
    padding: var(--spacing-medium);
    gap: var(--spacing-small)
}

.user-name {
    font-size: var(--font-size);
    color: var(--text-color);
    font-weight: bold;
}

.auth-button {
    display: flex;
    align-items: center;
    background-color: var(--background-color);
    color: var(--text-color);
    border: 1px solid var(--border-color);
    border-radius: 4px;
    padding: var(--spacing-small) var(--spacing-medium);
    cursor: pointer;
    transition: background-color var(--transition-duration, 0.3s), color var(--transition-duration, 0.3s);
}

.auth-button:hover {
    background-color: rgb(0, 0, 0, 0.1);
    color: var(--background-color);
}

.auth-icon {
    width: 16px;
    height: 16px;
    margin-left: var(--spacing-small);
    margin-right: var(--spacing-small);
    filter: var(--icon-filter);
}
</style>