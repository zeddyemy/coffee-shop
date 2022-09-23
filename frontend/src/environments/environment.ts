/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-0oy17auw.us', // the auth0 domain prefix
    audience: 'coffe', // the audience set for the auth0 app
    clientId: '6oDgbgkUvG7Bngg65lglihKZfBHh6jcP', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8100', // the base url of the running ionic application. 
  }
};
