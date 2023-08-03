import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";

import * as camelcaseKeys from "camelcase-keys";
import { Observable } from "rxjs";
import { map } from "rxjs/operators";

import { environment } from "../../environments/environment";
import {NewUserDetails, User, UserListItem, UserUpdate} from "../types/user";

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
      legal_status: user.legalStatus,
      gender: user.gender,
      race: user.race,
      has_phd: user.hasPhd,
      year_of_phd_completion: user.yearOfPhdCompletion,
    };

    return this.http
      .post<User>(uri, newUserDetails, { headers })
      .pipe(map((user) => camelcaseKeys(user, { deep: true })));
  }

  /**
   * Update user details for given user
   */
  updateUser(userId: number, userUpdate: UserUpdate): Observable<User> {
    const uri = environment.apiUrl + "/users/" + userId.toString();

    const headers = new HttpHeaders({
      "Content-type": "application/json",
    });

    const newUserDetails = {
      password: userUpdate.password,
      email: userUpdate.email,
      given_name: userUpdate.givenName,
      family_name: userUpdate.familyName,
      legal_status: userUpdate.legalStatus,
      gender: userUpdate.gender,
      race: userUpdate.race,
      has_phd: userUpdate.hasPhd,
      year_of_phd_completion: userUpdate.yearOfPhdCompletion,
    };

    return this.http
      .patch<User>(uri, newUserDetails, { headers })
      .pipe(map((user) => camelcaseKeys(user, { deep: true })));

  }
}
