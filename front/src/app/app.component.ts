import { Component, OnInit } from '@angular/core';
import { io } from 'socket.io-client';
import { SocketioService } from './services/socketio.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit{
  title = 'front';
  numero: number = 0

  constructor(
  ){}

  ngOnInit(): void {
    const socket = io(`ws://${"localhost"}:${3000}`, {
      transports: ['websocket', 'polling', 'flashsocket']
    })


    socket.on("connect", () => { console.log("Connected", socket.id) });
    socket.on("response", () => { console.log("Response", socket.id) });
    socket.on("contador", data => {
      this.numero = data as number
    });
  }
}
