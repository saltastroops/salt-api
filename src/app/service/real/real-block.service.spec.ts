import {
  HttpClientTestingModule,
  HttpTestingController,
} from "@angular/common/http/testing";
import { TestBed } from "@angular/core/testing";

import { environment } from "../../../environments/environment";
import { Block } from "../../types/block";
import { RealBlockService } from "./real-block.service";

describe("RealBlockService", () => {
  let service: RealBlockService;
  let httpTestingController: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
    });
    httpTestingController = TestBed.inject(HttpTestingController);
    service = TestBed.inject(RealBlockService);
  });

  it("should be created", () => {
    expect(service).toBeTruthy();
  });

  it("should return the content returned by the server", () => {
    const url = environment.apiUrl + "/blocks/4287";
    const testData = { id: 4287, name: "Block 4287" } as Block;

    service.getBlock(4287).subscribe((data) => {
      expect(data).toEqual(testData);
    });

    const req = httpTestingController.expectOne(url);
    req.flush(testData);
  });

  it("should raise an error", () => {
    const url = environment.apiUrl + "/blocks/4287";
    const errorMessage = "The server did not like this request.";

    service.getBlock(4287).subscribe(
      () => fail("Should have failed with an error."),
      () => {
        // Ideally we would test for the error (message). But it seems the HTTP testing
        // client does not use the HTTP interceptor, and hence we cannot really do this.
      },
    );

    const req = httpTestingController.expectOne(url);
    req.flush(errorMessage, { status: 400, statusText: "Bad Request" });
  });
});