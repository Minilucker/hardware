<!-- Brouillon d'application php pour potentiellement interagir avec la db via le wifi depuis l'esp32, abandonné au profit de l'UART -->

<?php
    class Rfid {
        private int $id;
        private int $identifier;
        private bool $revoked;

        public function __construct(int $id, int $identifier, bool $revoked) {
            $this->setId($id);
            $this->setIdentifier($identifier);
            $this->setRevoked($revoked);
        }

        public function getId(): int {
            return $this->id;
        }

        public function getIdentifier(): int {
            return $this->identifier;
        }

        public function getRevoked(): bool {
            return $this->revoked;
        }

        private function setId(int $id): void {
            $this->id = $id;
        }

        private function setIdentifier(int $identifier): void {
            $this->identifier = $identifier;
        }

        private function setRevoked(bool $revoked): void {
            $this->revoked = $revoked;
        }
    }

    try {
        $pdo = new PDO('mysql:host=localhost;dbname=rfid', 'root', '');

    } catch (PDOException $e) {
        die("error: ".$e);
    }
    if (preg_match('/^[0-9]*$/', $_GET['identifier'], $match)) {
        $payload = $_GET['identifier'];
        $query = $pdo->prepare('SELECT * FROM idtable WHERE identifier=:identifier');
        $query->bindValue(':identifier', $payload);
        $query->execute();
        
        $results = $query->fetch(PDO::FETCH_ASSOC);

        if($results) {
            $rfid = new Rfid($results["id"], $results["identifier"], $results["revoked"]);
            if ($rfid->getRevoked()){
                echo "identifier ".$rfid->getIdentifier()." has been revoked, be gone.";
            } else {
                echo "identifier ".$rfid->getIdentifier()." found and is valid";
            }
            exit();
        }
        echo 'Identifier not found, Not authorized';
    } else {
        die("not authorized");
    }
    
    
?>