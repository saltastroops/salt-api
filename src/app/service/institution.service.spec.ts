import { TestBed } from "@angular/core/testing";

import { InstitutionService } from "./institution.service";
import {HttpClient, HttpHandler} from "@angular/common/http";

describe("InstitutionService", () => {
  let service: InstitutionService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [HttpClient, HttpHandler]
    });
    service = TestBed.inject(InstitutionService);
  });

  it("should be created", () => {
    expect(service).toBeTruthy();
  });
});
