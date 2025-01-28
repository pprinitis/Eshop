// adminAuth.js (for demonstration only)
export async function getAdminToken() {
    // If using username/password grant:
    const tokenUrl = `${import.meta.env.VITE_KEYCLOAK_URL}realms/${import.meta.env.VITE_KEYCLOAK_REALM}/protocol/openid-connect/token`;
    
    const params = new URLSearchParams();
    params.append("grant_type", "client_credentials");
    params.append("client_id", import.meta.env.VITE_KEYCLOAK_PRIVATE_CLIENT_ID); // or your admin client
    params.append("client_secret", import.meta.env.VITE_KEYCLOAK_PRIVATE_CLIENT_ID); // or your admin client
    
    const response = await fetch(tokenUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: params,
    });

  
    if (!response.ok) {
      const text = await response.text();
      throw new Error(`Failed to get admin token: ${text}`);
    }
  
    const data = await response.json();
    return data.access_token;  // We'll use only the access token
  }
  