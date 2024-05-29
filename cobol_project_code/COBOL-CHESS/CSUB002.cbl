      ******************************************************************
      * Author:
      * Date:
      * Purpose:
      * Tectonics: cobc
      ******************************************************************
       IDENTIFICATION DIVISION.
      *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
       PROGRAM-ID. CSUB002.
       ENVIRONMENT DIVISION.
      *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
       CONFIGURATION SECTION.
      *-----------------------
       INPUT-OUTPUT SECTION.

       FILE-CONTROL.
           SELECT INFILE ASSIGN TO
           "C:\Users\xxbystea\CHESS_SAVE.txt"
           ORGANIZATION IS LINE SEQUENTIAL
           .
      *-----------------------
       DATA DIVISION.
      *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
       FILE SECTION.
       FD INFILE.
       01 MY-RECORD PIC X(200).
      *-----------------------
       WORKING-STORAGE SECTION.
       01 COUNTERS.
           05 COUNTER          PIC 99.
           05 COUNTER2         PIC 99.
       01 SWITCHES.
           05 SWITCH-EOF       PIC X.
               88 EOF-Y        VALUE 'Y'.
               88 NOT-EOF      VALUE 'N'.
      *INPUT AREA
       01 I-INPUT-AREA.
           05 I-INPUT OCCURS 32 TIMES.
               10 IN-ID        PIC S99.
               10 FILLER       PIC X VALUE SPACE.
               10 IN-X         PIC S99.
               10 FILLER       PIC X VALUE SPACE.
               10 IN-Y         PIC S99.
               10 FILLER       PIC X VALUE SPACE.
               10 IN-NAME      PIC XX.
               10 FILLER       PIC X VALUE SPACE.
               10 IN-FIRST     PIC X.


       LINKAGE SECTION.
       01 PLAYER-TURN          PIC X(1).
               88 W-TURN       VALUE 'W'.
               88 B-TURN       VALUE 'B'.
           COPY COORDINATES.
      *-----------------------
       PROCEDURE DIVISION USING COORDINATES
                                PLAYER-TURN.
      *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-
       MAIN-PROCEDURE.

           PERFORM A-INIT
           PERFORM B-MAIN

           GOBACK.

           A-INIT SECTION.
           INITIALIZE I-INPUT-AREA
                       SWITCHES
                       COUNTERS
                       MY-RECORD
           .
           B-MAIN SECTION.
           PERFORM C-OPEN-FILE
           PERFORM D-MOVE
           GOBACK.

           C-OPEN-FILE SECTION.

      *******************************************************************
      *                       C-OPEN-FILE SECTION                       *
      *******************************************************************

           MOVE 1 TO COUNTER
           OPEN I-O INFILE
           READ INFILE INTO PLAYER-TURN
           DISPLAY PLAYER-TURN
           READ INFILE INTO I-INPUT(COUNTER)
           PERFORM UNTIL EOF-Y OR COUNTER = 32
               ADD 1 TO COUNTER
               READ INFILE INTO I-INPUT(COUNTER)

               AT END
                   SET EOF-Y TO TRUE

               END-READ

           END-PERFORM
           CLOSE INFILE
           .

           D-MOVE SECTION.

      *******************************************************************
      *                         D-MOVE SECTION                          *
      *******************************************************************
           MOVE 1 TO COUNTER2
           MOVE 1 TO COUNTER
           PERFORM UNTIL COUNTER2 > 16
               MOVE IN-X(COUNTER) TO W-X-VAR(COUNTER)
               MOVE IN-Y(COUNTER) TO W-Y-POS(COUNTER)
               MOVE IN-NAME(COUNTER) TO W-PIECE(COUNTER)
               MOVE IN-FIRST(COUNTER) TO W-FIRST(COUNTER)
               ADD 1 TO COUNTER2
                        COUNTER
           END-PERFORM
           MOVE 1 TO COUNTER
           PERFORM UNTIL COUNTER2 > 32
               MOVE IN-X(COUNTER2) TO B-X-VAR(COUNTER)
               MOVE IN-Y(COUNTER2) TO B-Y-POS(COUNTER)
               MOVE IN-NAME(COUNTER2) TO B-PIECE(COUNTER)
               MOVE IN-FIRST(COUNTER2) TO B-FIRST(COUNTER)
               ADD 1 TO COUNTER2
                        COUNTER
           END-PERFORM
           .
