@extends('layouts.app')

@section('content')
    <h1>Notas</h1>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Título</th>
                <th>Contenido</th>
                <th>Estado</th>
            </tr>
        </thead>
        <tbody>
            @foreach ($notes as $note)
                <tr>
                    <td>{{ $note->id }}</td>
                    <td>{{ $note->title }}</td>
                    <td>{{ $note->content }}</td>
                    <td>{{ $note->status }}</td>
                </tr>
            @endforeach
        </tbody>
    </table>
@endsection