import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
@Injectable({
  providedIn: 'root'
})
export class RestService {

  constructor(private http: HttpClient) { }

  public post(url: string, data: any) {
    return this.http.post(url, data);
  }
  public get(url: string) {
    return this.http.get(url);
  }
}
