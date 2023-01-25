import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";

import * as camelcaseKeys from "camelcase-keys";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

import { environment } from "../../environments/environment";
import { NewUserDetails, User, UserListItem } from "../types/user";

@Injectable({
  providedIn: "root",
})
export class UserService {
  constructor(private http: HttpClient) {}

  /**
   * Get the user details for a given user
   */
  getUserById(user_id: number): Observable<User> {
    const uri = environment.apiUrl + "/users/" + user_id.toString();
    return this.http
      .get<User>(uri)
      .pipe(map((user) => camelcaseKeys(user, { deep: true })));
  }

  /**
   * Get the list of all Web Manager users
   */
  getUsers(): Observable<UserListItem[]> {
    const uri = environment.apiUrl + "/users/";
    return this.http
      .get<UserListItem[]>(uri)
      .pipe(
        map((users: UserListItem[]) =>
          users.map((user: UserListItem) =>
            camelcaseKeys(user, { deep: true }),
          ),
        ),
      );
  }

  /**
   * Create a user for given user details
   */
  createUser(user: NewUserDetails): Observable<User> {
    const uri = environment.apiUrl + "/users/";

    const headers = new HttpHeaders({
      "Content-type": "application/json",
    });

    const newUserDetails = {
      username: user.username,
      password: user.password,
      email: user.email,
      given_name: user.givenName,
      family_name: user.familyName,
      institution_id: user.institutionId,
    };

    return this.http
      .post<User>(uri, newUserDetails, { headers })
      .pipe(map((user) => camelcaseKeys(user, { deep: true })));
  }
}
