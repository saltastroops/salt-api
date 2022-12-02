import {
  getResponse,
  recordedResponses,
  saveAlias,
  saveResponse,
} from "./utils";

const recordHttpConfig = Cypress.env("recordHttpConfig") || {};
const mockIntercepts = recordHttpConfig.mockIntercepts || false;

function getTokenData() {
  const currentDate = new Date();
  const expiryDate = new Date(
    currentDate.getTime() + 1000000 * 24 * 60 * 60000,
  );
  const token = "secret";

  return {
    access_token: token,
    // eslint-disable-next-line @typescript-eslint/ban-ts-comment
    // @ts-ignore
    expires_at: expiryDate,
    token_type: "bearer",
  };
}

Cypress.Commands.add("recordHttp", (url) => {
  return cy.intercept(url, (request) => {
    const requestKey = `${request.method}-${request.url}`;
    request.alias = `${requestKey}-${Cypress._.random(1e6)}`;
    const key = request.alias;
    saveAlias(key);

    if (mockIntercepts) {
      const responseKey = Object.keys(recordedResponses).find((k) =>
        k.includes(requestKey),
      );
      const response = JSON.parse(getResponse(responseKey));

      // set the mock response's date to the current time.
      const date = new Date();
      response.headers.date = date.toString();

      if ("set-cookie" in response.headers) {
        // There can be a session and a secondary auth toke cooke.
        // However, Cypress can handle a single cookie only.
        // We thus discard the session cookie, which is not needed when mocking.
        const cookies = response.headers["set-cookie"];
        if (Object.keys(cookies).length > 1) {
          console.warn("One or more cookies are ignored.");
        }
        const cookieEntries = cookies.entries();
        delete response.headers["set-cookie"];
        for (const [, cookie] of cookieEntries) {
          if (cookie.includes("secondary_auth_token=")) {
            response.headers["set-cookie"] = cookie;
            break;
          }
        }
      }

      request.reply(response);
    } else {
      request.continue((response) => {
        if (request.url.includes("token")) {
          const tokenResponse = { ...response };
          if (response.statusCode == 200) {
            tokenResponse.body = getTokenData();
            saveResponse(key, JSON.stringify(tokenResponse));
          } else {
            saveResponse(key, JSON.stringify(response));
          }
        } else {
          saveResponse(key, JSON.stringify(response));
        }
      });
    }
  });
});
