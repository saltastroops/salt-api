import {
  HttpClientTestingModule,
  HttpTestingController,
} from "@angular/common/http/testing";
import { TestBed } from "@angular/core/testing";

import { MosService } from "./mos.service";

describe("RealBlockService", () => {
  let service: MosService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
    });
    TestBed.inject(HttpTestingController);
    service = TestBed.inject(MosService);
  });

  it("should be created", () => {
    expect(service).toBeTruthy();
  });
});
