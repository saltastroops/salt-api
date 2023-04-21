import "cypress-network-idle";
import { STATUS_CODES } from "http";

// Taken from https://gist.github.com/TooTallNate/4fd641f820e1325695487dfd883e5285#file-http-error-js
class HTTPError extends Error {
  private statusCode: number;
  constructor(code: number, message: string) {
    super(message || STATUS_CODES[code]);
    this.statusCode = code;
  }
}
export default HTTPError;

beforeEach(() => {
  cy.task("clearEmailInbox");
});
