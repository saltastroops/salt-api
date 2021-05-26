# Developing the Web Manager Frontend

This page outlines how to develop the Web Manager frontend.

## Requirements

You need to have the following installed on your machine.

* [NodeJS](https://nodejs.org/en/) 12 or higher

## Installation

Clone the repository.

```shell
git clone git@github.com:saltastroops/web-manager-2021.git web-manager
```

!!! tip
You may call the created directory whatever you want. However, the following instructions assume it is called `web-manager`.

Go to the directory `web-manager/frontend` and install the required packages.

```bash
cd web-manager/frontend
npm install
```

You can now start the development server.

```bash
ng serve -o
```

The flag `-o` tells `ng` to automatically open a browser window once the code has been compiled. If you make changes to project files, the code is automatically recompiled and the page content is updated in the browser. However, the latter seems to be buggy in Safari, so you might want to use Firefox or Chrome instead.

## Creating new files

Wherever possible, new files should always be created using the `ng generate` command.

## Styling

[Bulma](https://bulma.io) is used for styling, and its classes should be used wherever possible. This is particularly true for colours; custom colours should be avoided as much as possible.

## Asynchronous code

Generally, asynchronous code such as HTTP requests are described by means of three different aspects - a loading flag, errors and (non-error) content. Each of these should have its own RxJS observable, such as `isLoading$`, `error$` and `content$`. See the block view component (`src/app/proposal/block-view/block-view.component.ts`) for an example, and [this blog post](https://blog.eyas.sh/2020/05/better-loading-and-error-handling-in-angular/) for more explanation.

## Testing

[Angular Testing Library](https://testing-library.com/docs/angular-testing-library/intro) should be used for testing components.

