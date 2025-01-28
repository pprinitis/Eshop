// assignUserRole.js
import { getAdminToken } from "./adminKeycloak";

export async function assignRoleToUser(username, roleName) {
  const adminToken = await getAdminToken();

  const userSearchUrl = `${import.meta.env.VITE_KEYCLOAK_URL}admin/realms/${import.meta.env.VITE_KEYCLOAK_REALM}/users?username=${encodeURIComponent(username)}`;
  const userResp = await fetch(userSearchUrl, {
    headers: { Authorization: `Bearer ${adminToken}` },
  });
  if (!userResp.ok) {
    const errorText = await userResp.text();
    throw new Error(`Failed to look up user: ${errorText}`);
  }
  const users = await userResp.json();
  if (!users.length) {
    throw new Error(`User not found for username="${username}"`);
  }
  const userId = users[0].id;

  const roleUrl = `${import.meta.env.VITE_KEYCLOAK_URL}admin/realms/${import.meta.env.VITE_KEYCLOAK_REALM}/roles/${encodeURIComponent(roleName)}`;
  const roleResp = await fetch(roleUrl, {
    headers: { Authorization: `Bearer ${adminToken}` },
  });
  if (!roleResp.ok) {
    const errorText = await roleResp.text();
    throw new Error(`Could not find role "${roleName}": ${errorText}`);
  }
  const roleObj = await roleResp.json();

  const assignUrl = `${import.meta.env.VITE_KEYCLOAK_URL}admin/realms/${import.meta.env.VITE_KEYCLOAK_REALM}/users/${userId}/role-mappings/realm`;
  const assignResp = await fetch(assignUrl, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${adminToken}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify([{ id: roleObj.id, name: roleObj.name }]),
  });
  if (!assignResp.ok) {
    const errorText = await assignResp.text();
    throw new Error(`Failed to assign role: ${errorText}`);
  }
  return `Assigned role "${roleObj.name}" to user "${username}" successfully.`;
}
