const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

/**
 * Single low-level fetch wrapper. Every API call in the app goes
 * through this function so error handling and JSON parsing stay
 * consistent across pages.
 */
async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch (networkError) {
    // fetch() itself throws only on network-level failure (backend down,
    // DNS failure, CORS block) - not on 4xx/5xx responses.
    throw new ApiError("Could not reach the SkillGraph API. Is the backend running?", 0);
  }

  let body = null;
  try {
    body = await response.json();
  } catch {
    // Response had no JSON body - leave body as null.
  }

  if (!response.ok) {
    const message = body?.detail || `Request failed with status ${response.status}`;
    throw new ApiError(message, response.status);
  }

  return body;
}

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

export const api = {
  getHealth: () => request("/api/health"),
  getCareers: () => request("/api/careers"),
  getCareer: (careerId) => request(`/api/careers/${encodeURIComponent(careerId)}`),
  getSkills: () => request("/api/skills"),
  getSkill: (skillId) => request(`/api/skills/${encodeURIComponent(skillId)}`),
  postSkillGap: (payload) =>
    request("/api/skill-gap", { method: "POST", body: JSON.stringify(payload) }),
  getLearningPath: (fromSkillId, toSkillId) =>
    request(
      `/api/learning-path?from_skill_id=${encodeURIComponent(fromSkillId)}&to_skill_id=${encodeURIComponent(toSkillId)}`
    ),
};
