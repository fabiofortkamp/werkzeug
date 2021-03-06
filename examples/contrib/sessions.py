#!/usr/bin/env python
# -*- coding: utf-8 -*-
from werkzeug.contrib.sessions import SessionMiddleware
from werkzeug.contrib.sessions import SessionStore
from werkzeug.serving import run_simple


class MemorySessionStore(SessionStore):
    def __init__(self, session_class=None):
        SessionStore.__init__(self, session_class=None)
        self.sessions = {}

    def save(self, session):
        self.sessions[session.sid] = session

    def delete(self, session):
        self.sessions.pop(session.id, None)

    def get(self, sid):
        if not self.is_valid_key(sid) or sid not in self.sessions:
            return self.new()
        return self.session_class(self.sessions[sid], sid, False)


def application(environ, start_response):
    session = environ["werkzeug.session"]
    session["visit_count"] = session.get("visit_count", 0) + 1

    start_response("200 OK", [("Content-Type", "text/html")])
    return [
        """<!doctype html>
        <title>Session Example</title>
        <h1>Session Example</h1>
        <p>You visited this page %d times.</p>"""
        % session["visit_count"]
    ]


def make_app():
    return SessionMiddleware(application, MemorySessionStore())


if __name__ == "__main__":
    run_simple("localhost", 5000, make_app())
