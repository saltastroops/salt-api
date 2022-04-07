import { HttpClient } from "@angular/common/http";
import {
  HttpClientTestingModule,
  HttpTestingController,
} from "@angular/common/http/testing";
import { TestBed } from "@angular/core/testing";

import { MosService } from "../service/mos.service";

describe("MosComponent", () => {
  let service: MosService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [HttpClient],
    });
    TestBed.inject(HttpTestingController);
    service = TestBed.inject(MosService);
  });

  it("should create", () => {
    expect(service).toBeTruthy();
  });
});
