declare namespace Cypress {
  interface Chainable {
    forceNetworkError(): Chainable;
    forceServerError(): Chainable;
  }
}

// Import commands.js using ES2015 syntax:
import './commands';
