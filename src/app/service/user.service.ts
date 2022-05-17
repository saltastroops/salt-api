import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";

import * as camelcaseKeys from "camelcase-keys";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

import { environment } from "../../environments/environment";
import { User, UserListItem } from "../types/user";

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
}
